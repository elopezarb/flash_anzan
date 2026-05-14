(function () {
  "use strict";

  const pasos = [
    "Paso 1-3",
    "Paso 2-4",
    "Paso 5",
    "Paso 6",
    "Paso 7",
    "Paso 8",
    "Paso 9",
    "Paso 10",
    "Paso 11.1",
    "Paso 11.2",
    "Paso 12.1",
    "Paso 12.2",
  ];

  const stepNumbers = Object.fromEntries(pasos.map((step, index) => [step, index + 1]));
  const reverseSteps = Object.fromEntries(Object.entries(stepNumbers).map(([key, value]) => [value, key]));
  const sumSteps = new Set([1, 3, 5, 7, 9, 11]);

  class SorobanOperationGenerator {
    constructor({ step, digits, firstOpDigits, onlySum, difficulty }) {
      this.step = step;
      this.digits = digits;
      this.firstOpDigits = firstOpDigits || digits;
      this.onlySum = onlySum;
      this.difficulty = difficulty || "balanced";
      this.resta = !sumSteps.has(stepNumbers[step]);
      this.stepsRules = window.SOROBAN_RULES.steps;
      this.weightRules = window.SOROBAN_RULES.weights;
      this.extraConditions = {};
      this.currentOperationUsesTargetLevel = false;
    }

    getFirstOperation() {
      return Array.from({ length: this.firstOpDigits }, () => randomInt(1, 9));
    }

    static carryNormalize(values, base = 10) {
      const normalized = Array(values.length).fill(0);
      let carry = 0;

      for (let index = values.length - 1; index >= 0; index -= 1) {
        const total = values[index] + carry;
        normalized[index] = modulo(total, base);
        carry = Math.floor(total / base);
      }

      const prefix = [];
      while (carry > 0) {
        prefix.unshift(carry % base);
        carry = Math.floor(carry / base);
      }

      return prefix.concat(normalized);
    }

    getSumNum(step, position, currentDigit) {
      if (stepNumbers[step] > 4) {
        if (position > 0) {
          if (this.extraConditions[step]) {
            return this.weightedDigit(step, currentDigit);
          }
          return this.getSumNum(reverseSteps[stepNumbers[step] - 2], position, currentDigit);
        }
        return this.weightedDigit(step, currentDigit);
      }

      return this.weightedDigit(step, currentDigit);
    }

    getRestNum(step, position, currentDigit) {
      if (stepNumbers[step] > 4) {
        if (position > 0) {
          if (this.extraConditions[step]) {
            return -this.weightedDigit(step, currentDigit);
          }
          return this.getRestNum(reverseSteps[stepNumbers[step] - 2], position, currentDigit);
        }
        return this.getRestNum(reverseSteps[stepNumbers[step] - 2], position, currentDigit);
      }

      return -this.weightedDigit(step, currentDigit);
    }

    weightedDigit(step, currentDigit) {
      const digitKey = String(currentDigit);
      const options = this.stepsRules[step][digitKey] || [0];
      const weights = this.weightRules[step][digitKey] || options.map(() => 1);
      if (step === this.step) {
        this.currentOperationUsesTargetLevel = true;
      }
      return weightedChoice(options, weights, this.difficulty, currentDigit);
    }

    getNextOperation(sumComplete, nextSum) {
      let restStep;
      let sumStep;
      this.currentOperationUsesTargetLevel = false;

      if (this.resta) {
        restStep = this.step;
        sumStep = reverseSteps[stepNumbers[this.step] - 1];
      } else {
        sumStep = this.step;
        restStep = reverseSteps[stepNumbers[this.step] - 1];
      }

      const shouldChange = {
        "Paso 1-3": oneInSix() || countDigit(sumComplete, 9) > 1,
        "Paso 2-4": !oneInSix() && countDigit(sumComplete, 0) < 1,
        "Paso 5": oneInSix() || countDigit(sumComplete, 9) > 1,
        "Paso 6": !oneInSix() && countDigit(sumComplete, 0) < 1,
        "Paso 7": oneInSix() || countDigit(sumComplete, 9) > 1,
        "Paso 8": !oneInSix() && countDigit(sumComplete, 0) < 1,
        "Paso 9": oneInSix() || countDigit(sumComplete, 9) > 1,
        "Paso 10": !oneInSix() && countDigit(sumComplete, 0) < 1,
        "Paso 11.1": oneInSix() || countDigit(sumComplete, 9) > 1,
        "Paso 11.2": !oneInSix() && countDigit(sumComplete, 0) < 1,
        "Paso 12.1": oneInSix() || countDigit(sumComplete, 9) > 1,
        "Paso 12.2": !oneInSix() && countDigit(sumComplete, 0) < 1,
      };

      const useRest = Boolean(restStep) && shouldChange[this.step] && !this.onlySum;

      for (let offset = this.digits; offset > 0; offset -= 1) {
        const j = sumComplete.length - offset;
        const currentValue = sumComplete[j];
        const position = sumComplete.indexOf(currentValue);
        const previousDigit = pythonIndex(sumComplete, position - 1);

        this.extraConditions = {
          "Paso 1-3": true,
          "Paso 2-4": true,
          "Paso 5": true,
          "Paso 6": true,
          "Paso 7": ![4, 9].includes(previousDigit),
          "Paso 8": ![0, 5].includes(previousDigit),
          "Paso 9": ![4, 9].includes(previousDigit),
          "Paso 10": ![0, 5].includes(previousDigit),
          "Paso 11.1": previousDigit !== 9,
          "Paso 11.2": previousDigit !== 0,
          "Paso 12.1": true,
          "Paso 12.2": sumComplete[0] !== 0,
        };

        const operationDigit = useRest
          ? this.getRestNum(restStep, position, currentValue)
          : this.getSumNum(sumStep, position, currentValue);

        nextSum[nextSum.length - offset] = operationDigit;
        sumComplete[j] = currentValue + operationDigit;
        sumComplete = SorobanOperationGenerator.carryNormalize(sumComplete);
      }

      return [nextSum.slice(), sumComplete, this.currentOperationUsesTargetLevel];
    }

    getListOfOperations(operationCount) {
      let sumComplete = this.getFirstOperation();
      let nextSum = Array(sumComplete.length).fill(0);
      const fullSum = [sumComplete.slice()];
      let levelHits = 0;

      for (let index = 0; index < operationCount; index += 1) {
        const result = this.getNextOperation(sumComplete, nextSum);
        nextSum = result[0];
        sumComplete = result[1];
        if (result[2]) {
          levelHits += 1;
        }
        fullSum.push(nextSum.slice());
      }

      return {
        operations: fullSum,
        resultDigits: sumComplete,
        result: operationToInt(sumComplete),
        levelHits,
      };
    }
  }

  const elements = {
    modeSelect: document.getElementById("modeSelect"),
    stepSelect: document.getElementById("stepSelect"),
    digitsInput: document.getElementById("digitsInput"),
    firstDigitsInput: document.getElementById("firstDigitsInput"),
    operationsInput: document.getElementById("operationsInput"),
    questionsInput: document.getElementById("questionsInput"),
    speedInput: document.getElementById("speedInput"),
    onlySumInput: document.getElementById("onlySumInput"),
    difficultySelect: document.getElementById("difficultySelect"),
    forceLevelInput: document.getElementById("forceLevelInput"),
    startButton: document.getElementById("startButton"),
    revealButton: document.getElementById("revealButton"),
    answerForm: document.getElementById("answerForm"),
    answerInput: document.getElementById("answerInput"),
    submitAnswer: document.getElementById("submitAnswer"),
    feedback: document.getElementById("feedback"),
    flashNumber: document.getElementById("flashNumber"),
    flashSign: document.getElementById("flashSign"),
    progressDots: document.getElementById("progressDots"),
    operationList: document.getElementById("operationList"),
    roundCount: document.getElementById("roundCount"),
    bestStreak: document.getElementById("bestStreak"),
  };

  const state = {
    currentRound: null,
    timer: null,
    rounds: 0,
    streak: 0,
    bestStreak: 0,
    operationQuiz: null,
  };

  pasos.forEach((step) => {
    const option = document.createElement("option");
    option.value = step;
    option.textContent = step;
    if (step === "Paso 8") {
      option.selected = true;
    }
    elements.stepSelect.append(option);
  });

  elements.modeSelect.addEventListener("change", syncMode);
  elements.startButton.addEventListener("click", startRound);
  elements.revealButton.addEventListener("click", revealAnswer);
  elements.answerForm.addEventListener("submit", checkAnswer);
  syncMode();

  function startRound() {
    window.clearTimeout(state.timer);
    clearFeedback();

    const settings = readSettings();
    if (settings.mode === "operations") {
      startOperationsQuiz(settings);
      return;
    }

    state.operationQuiz = null;
    state.currentRound = generateRound(settings);
    state.currentRound.visibleIndex = -1;

    elements.answerInput.value = "";
    elements.answerInput.disabled = true;
    elements.submitAnswer.disabled = true;
    elements.revealButton.disabled = true;
    elements.startButton.disabled = true;
    elements.flashNumber.textContent = "3";
    elements.flashSign.textContent = "Preparado";

    renderHistory(false);
    renderDots(state.currentRound.operations.length, 0);

    countdown(3, () => playOperations(settings.speed));
  }

  function startOperationsQuiz(settings) {
    state.rounds = 0;
    state.streak = 0;
    state.bestStreak = 0;
    state.operationQuiz = {
      settings,
      columns: [],
      currentQuestion: 0,
      totalQuestions: settings.questionCount,
      score: 0,
    };
    renderStats();
    nextOperationsQuestion();
  }

  function nextOperationsQuestion() {
    const quiz = state.operationQuiz;
    if (!quiz || quiz.currentQuestion >= quiz.totalQuestions) {
      finishOperationsQuiz();
      return;
    }

    clearFeedback();
    state.currentRound = generateRound(quiz.settings);
    quiz.columns.push({
      operations: state.currentRound.operations,
      result: state.currentRound.result,
      userAnswer: null,
      correct: null,
    });
    quiz.currentQuestion += 1;

    elements.flashNumber.textContent = "";
    elements.flashSign.textContent = "";
    elements.answerInput.value = "";
    elements.answerInput.disabled = false;
    elements.submitAnswer.disabled = false;
    elements.revealButton.disabled = true;
    elements.startButton.disabled = true;
    elements.answerInput.focus();
    renderOperationBoard();
  }

  function countdown(value, done) {
    if (value === 0) {
      done();
      return;
    }

    elements.flashNumber.textContent = String(value);
    state.timer = window.setTimeout(() => countdown(value - 1, done), 520);
  }

  function playOperations(speed) {
    const operations = state.currentRound.operations;
    let index = 0;

    const showNext = () => {
      if (index >= operations.length) {
        elements.flashNumber.textContent = "?";
        elements.flashSign.textContent = "Escribe el resultado";
        elements.answerInput.disabled = false;
        elements.submitAnswer.disabled = false;
        elements.revealButton.disabled = false;
        elements.startButton.disabled = false;
        elements.answerInput.focus();
        return;
      }

      state.currentRound.visibleIndex = index;
      const operation = operationToInt(operations[index]);
      elements.flashNumber.textContent = operation < 0 ? `-${Math.abs(operation)}` : String(operation);
      elements.flashSign.textContent = index === 0 ? "inicio" : operation >= 0 ? "suma" : "resta";
      renderDots(operations.length, index + 1);
      index += 1;
      state.timer = window.setTimeout(showNext, speed);
    };

    showNext();
  }

  function checkAnswer(event) {
    event.preventDefault();
    if (!state.currentRound) {
      return;
    }

    const answer = Number.parseInt(elements.answerInput.value, 10);
    if (Number.isNaN(answer)) {
      showFeedback("Escribe un numero.", "bad");
      return;
    }

    const correct = answer === state.currentRound.result;
    state.rounds += 1;
    state.streak = correct ? state.streak + 1 : 0;
    state.bestStreak = Math.max(state.bestStreak, state.streak);

    if (state.operationQuiz) {
      const column = state.operationQuiz.columns[state.operationQuiz.columns.length - 1];
      column.userAnswer = answer;
      column.correct = correct;
      if (correct) {
        state.operationQuiz.score += 1;
      }
      showFeedback(
        correct ? "Correcto." : `Resultado: ${state.currentRound.result}`,
        correct ? "good" : "bad"
      );
      renderStats();
      renderOperationBoard();
      elements.submitAnswer.disabled = true;
      elements.answerInput.disabled = true;

      if (state.operationQuiz.currentQuestion >= state.operationQuiz.totalQuestions) {
        finishOperationsQuiz();
      } else {
        state.timer = window.setTimeout(nextOperationsQuestion, 900);
      }
      return;
    }

    showFeedback(
      correct ? "Correcto." : `Resultado: ${state.currentRound.result}`,
      correct ? "good" : "bad"
    );
    renderStats();
    renderHistory(true);
    elements.submitAnswer.disabled = true;
    elements.answerInput.disabled = true;
  }

  function revealAnswer() {
    if (!state.currentRound) {
      return;
    }

    showFeedback(`Resultado: ${state.currentRound.result}`, "bad");
    state.streak = 0;
    renderStats();
    renderHistory(true);
    elements.submitAnswer.disabled = true;
    elements.answerInput.disabled = true;
  }

  function readSettings() {
    const digits = clampInt(elements.digitsInput.value, 1, 6);
    const firstOpDigits = Math.max(digits, clampInt(elements.firstDigitsInput.value, 1, 6));
    return {
      mode: elements.modeSelect.value,
      step: elements.stepSelect.value,
      digits,
      firstOpDigits,
      operationCount: clampInt(elements.operationsInput.value, 1, 30),
      questionCount: clampInt(elements.questionsInput.value, 1, 30),
      speed: clampFloat(elements.speedInput.value, 0.25, 5) * 1000,
      onlySum: elements.onlySumInput.checked,
      difficulty: elements.difficultySelect.value,
      forceLevel: elements.forceLevelInput.checked,
    };
  }

  function generateRound(settings) {
    let bestRound = null;
    for (let attempt = 0; attempt < 80; attempt += 1) {
      const generator = new SorobanOperationGenerator(settings);
      const round = generator.getListOfOperations(settings.operationCount - 1);
      bestRound = round;
      if (!settings.forceLevel || round.levelHits > 0 || stepNumbers[settings.step] <= 4) {
        return round;
      }
    }

    return bestRound;
  }

  function renderHistory(showAll) {
    elements.operationList.innerHTML = "";
    if (!state.currentRound || !showAll) {
      return;
    }

    state.currentRound.operations.forEach((operationDigits, index) => {
      const item = document.createElement("li");
      const operation = operationToInt(operationDigits);
      const sign = index === 0 ? "" : operation >= 0 ? "+ " : "- ";
      item.textContent = `${sign}${Math.abs(operation)}`;
      if (showAll || index <= state.currentRound.visibleIndex) {
        item.classList.add("visible");
      }
      elements.operationList.append(item);
    });
  }

  function renderOperationBoard() {
    const quiz = state.operationQuiz;
    if (!quiz) {
      return;
    }

    const board = document.createElement("div");
    board.className = "operation-board";

    const table = document.createElement("table");
    table.className = "operation-table";

    const header = document.createElement("tr");
    header.append(document.createElement("th"));
    quiz.columns.forEach((_, index) => {
      const th = document.createElement("th");
      th.textContent = String(index + 1);
      header.append(th);
    });
    table.append(header);

    for (let row = 0; row < quiz.settings.operationCount; row += 1) {
      const tr = document.createElement("tr");
      const label = document.createElement("td");
      label.className = "row-label";
      label.textContent = String(row + 1);
      tr.append(label);

      quiz.columns.forEach((column) => {
        const td = document.createElement("td");
        const operation = operationToInt(column.operations[row]);
        td.textContent = formatOperation(operation, row);
        tr.append(td);
      });
      table.append(tr);
    }

    const answerRow = document.createElement("tr");
    const label = document.createElement("td");
    label.className = "row-label";
    label.textContent = "Tu respuesta";
    answerRow.append(label);

    quiz.columns.forEach((column) => {
      const td = document.createElement("td");
      td.className = "answer-cell";
      if (column.userAnswer !== null) {
        td.textContent = String(column.userAnswer);
        td.classList.add(column.correct ? "correct" : "wrong");
      }
      answerRow.append(td);
    });
    table.append(answerRow);

    const expectedRow = document.createElement("tr");
    const expectedLabel = document.createElement("td");
    expectedLabel.className = "row-label";
    expectedLabel.textContent = "Respuesta";
    expectedRow.append(expectedLabel);

    quiz.columns.forEach((column) => {
      const td = document.createElement("td");
      td.className = "expected-cell";
      if (column.userAnswer !== null) {
        td.textContent = String(column.result);
      }
      expectedRow.append(td);
    });
    table.append(expectedRow);

    board.append(table);
    elements.progressDots.innerHTML = "";
    elements.flashNumber.replaceWith(board);
    elements.flashNumber = board;
  }

  function finishOperationsQuiz() {
    const quiz = state.operationQuiz;
    if (!quiz) {
      return;
    }

    elements.startButton.disabled = false;
    elements.submitAnswer.disabled = true;
    elements.answerInput.disabled = true;
    showFeedback(`Quiz terminado. Puntuacion: ${quiz.score}/${quiz.totalQuestions}`, "good");
  }

  function syncMode() {
    const operationsMode = elements.modeSelect.value === "operations";
    document.body.classList.toggle("operations-mode", operationsMode);
    window.clearTimeout(state.timer);
    clearFeedback();
    state.currentRound = null;
    state.operationQuiz = null;
    elements.answerInput.value = "";
    elements.answerInput.disabled = true;
    elements.submitAnswer.disabled = true;
    elements.revealButton.disabled = true;
    elements.startButton.disabled = false;
    resetStage();
    renderHistory(false);
    renderDots(0, 0);
  }

  function resetStage() {
    const currentStageContent = document.querySelector(".operation-board");
    if (currentStageContent) {
      const flashNumber = document.createElement("div");
      flashNumber.id = "flashNumber";
      flashNumber.className = "flash-number";
      flashNumber.textContent = "Listo";
      currentStageContent.replaceWith(flashNumber);
      elements.flashNumber = flashNumber;
      return;
    }

    elements.flashNumber.textContent = "Listo";
    elements.flashSign.textContent = "";
  }

  function formatOperation(operation, index) {
    if (index === 0) {
      return String(operation);
    }
    return operation < 0 ? `- ${Math.abs(operation)}` : `+ ${operation}`;
  }

  function renderDots(total, done) {
    elements.progressDots.innerHTML = "";
    for (let index = 0; index < total; index += 1) {
      const dot = document.createElement("span");
      if (index < done) {
        dot.classList.add("done");
      }
      elements.progressDots.append(dot);
    }
  }

  function renderStats() {
    elements.roundCount.textContent = String(state.rounds);
    elements.bestStreak.textContent = String(state.bestStreak);
  }

  function showFeedback(message, tone) {
    elements.feedback.textContent = message;
    elements.feedback.className = `feedback ${tone}`;
  }

  function clearFeedback() {
    elements.feedback.textContent = "";
    elements.feedback.className = "feedback";
  }

  function operationToInt(operation) {
    return operation.reduce((total, digit, index) => {
      return total + digit * 10 ** (operation.length - index - 1);
    }, 0);
  }

  function weightedChoice(options, weights, difficulty = "balanced", currentDigit = 0) {
    const tunedWeights = weights.map((weight, index) => {
      const option = Number(options[index] || 0);
      const baseWeight = Number(weight || 0);
      if (difficulty === "balanced") {
        return baseWeight;
      }

      const magnitude = Math.max(1, Math.abs(option));
      const boundaryMove = currentDigit + option >= 10 || currentDigit - option < 0;
      if (difficulty === "hard") {
        return baseWeight * magnitude ** 1.25 * (boundaryMove ? 1.8 : 1);
      }

      return baseWeight / (magnitude ** 1.15 * (boundaryMove ? 1.6 : 1));
    });
    const total = tunedWeights.reduce((sum, weight) => sum + Number(weight || 0), 0);
    if (total <= 0) {
      return Number(options[Math.floor(Math.random() * options.length)] || 0);
    }

    let threshold = Math.random() * total;
    for (let index = 0; index < options.length; index += 1) {
      threshold -= Number(tunedWeights[index] || 0);
      if (threshold <= 0) {
        return Number(options[index]);
      }
    }

    return Number(options[options.length - 1] || 0);
  }

  function oneInSix() {
    return randomInt(1, 6) === 2;
  }

  function countDigit(values, digit) {
    return values.filter((value) => value === digit).length;
  }

  function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  function clampInt(value, min, max) {
    const parsed = Number.parseInt(value, 10);
    if (Number.isNaN(parsed)) {
      return min;
    }
    return Math.min(max, Math.max(min, parsed));
  }

  function clampFloat(value, min, max) {
    const parsed = Number.parseFloat(value);
    if (Number.isNaN(parsed)) {
      return min;
    }
    return Math.min(max, Math.max(min, parsed));
  }

  function modulo(value, base) {
    return ((value % base) + base) % base;
  }

  function pythonIndex(values, index) {
    return values[index < 0 ? values.length + index : index];
  }
})();
