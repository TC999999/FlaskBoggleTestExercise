const $btn = $(".submit-word");
const $form = $("#word-form");
const $newWord = $("#new-word");
const $result = $("#result");
const $timer = $("#time-left");
const $start = $("#start");
const $scoreNum = $("#score-num");
const $reset = $("#reset");
const $gameNumber = $("#game-number");
const $boggleBoard = $("#boggle-board");
const $wordFormDiv = $("#word-form-div");
const $playerTimer = $("#player-timer");
const $playerScore = $("#player-score");
const $wordList = $("#word-list");

$btn.on("click", doNothing);

async function doNothing(e) {
  e.preventDefault();
}

async function wordHandling(e) {
  e.preventDefault();
  const $word = $newWord.val();
  wordData = $word;
  const res = await axios.post(`http://127.0.0.1:5000/checking`, {
    json: { wordData },
  });

  $newWord.val("");
  const results = await axios.get("http://127.0.0.1:5000/results/json");
  if (results.data.result === "ok") {
    $result.html(`<p class="correct">OK</p>`);
  } else if (results.data.result === "not-on-board") {
    $result.html(`<p class="incorrect">NOT ON BOARD</p>`);
  }
  if (results.data.result === "not-word") {
    $result.html(`<p class="notAWord">NOT A WORD</p>`);
  }
  await score();
  clearResults();
}

$start.on("click", countdown);

async function countdown() {
  $btn.off("click", doNothing);
  $start.off("click", countdown);
  $btn.on("click", wordHandling);
  $boggleBoard.removeClass("hidden");
  $wordFormDiv.removeClass("hidden");
  $playerTimer.removeClass("hidden");
  $playerScore.removeClass("hidden");
  $boggleBoard.addClass("showing");
  $wordFormDiv.addClass("showing");
  $playerTimer.addClass("showing");
  $playerScore.addClass("showing");

  $start.addClass("hidden");

  let start = 60;
  const time = setInterval(async function () {
    $timer.text(start);
    start--;
    if (start <= 9) {
      $timer.addClass("outOfTime");
    }
    if (start === -1) {
      $timer.text("YOUR TIME IS UP!");
      $btn.off("click", wordHandling);
      $btn.on("click", doNothing);
      $reset.removeClass("hidden");
      $reset.addClass("showing");
      $wordFormDiv.removeClass("showing");
      $wordFormDiv.addClass("hidden");
      const count = await axios.get("http://127.0.0.1:5000/count");
      await high_score();
      clearInterval(time);
    }
  }, 1000);
}

function clearResults() {
  let resTime = 2;
  const id = setInterval(function () {
    resTime--;
    if (resTime == 0) {
      $result.html("");
      clearInterval(id);
    }
  }, 1000);
}

async function score() {
  const score_arr = await axios.get("http://127.0.0.1:5000/score");
  //   console.log(score_arr.data);
  getWordList(score_arr.data);
  let total = 0;
  for (let word of score_arr.data) {
    total += word.length;
  }
  //   console.log(total);
  $scoreNum.text(total);
}

async function high_score() {
  let score = await axios.get("http://127.0.0.1:5000/score");

  let total = 0;
  for (let word of score.data) {
    total += word.length;
  }
  const highScore = await axios.post("http://127.0.0.1:5000/high_score", {
    json: { total },
  });
}

function getWordList(arr) {
  $wordList.html("");
  for (let item of arr) {
    let $wordItem = $("<li>").text(item);
    $wordList.append($wordItem);
  }
}
