document.addEventListener('DOMContentLoaded', function () {

    const testWordListContainer = document.querySelector("div.vocabulary-test-word-list");
    const currentTestWordContainer = document.querySelector("div.test-word-container");
    const testWordAnswerContainer = document.querySelector("div.test-word-answer-container");

    const correctAnswersColumn = document.querySelector("div.result-column.correct");
    const wrongAnswersColumn = document.querySelector("div.result-column.wrong");

    const userAnswerInput = testWordAnswerContainer.querySelector("input");

    const testButton = document.querySelector("button");
    testButton.addEventListener('click', function() { checkForMatch() });

    nextWord();
    userAnswerInput.value = "";

    function nextWord() {

        let testWord = testWordListContainer.firstElementChild;
        currentTestWordContainer.appendChild(testWord);
    }

    function moveWord( testedWordElem, destinationElem ) {

        destinationElem.appendChild(testedWordElem);
    }

    function checkForMatch() {

        let testedWordElem = currentTestWordContainer.firstElementChild;
        let testedWord = testedWordElem.innerText;
        let correctAnswer = currentTestWordContainer.firstElementChild.dataset.italian;
        let userAnswer = userAnswerInput.value;

        if ( userAnswer === correctAnswer ) {

            moveWord( testedWordElem, correctAnswersColumn);

        } else {

            moveWord( testedWordElem, wrongAnswersColumn );
        }

        nextWord();
        userAnswerInput.value = "";
    }
});