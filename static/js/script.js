document.addEventListener('DOMContentLoaded', function () {

    const revealedCardClassName = "revealed";
    const hiddenCardClassName = "hidden";
    const matchedCardClassName = "matched";

    let selectedCards = [];

    const cards = document.querySelectorAll(".card");

    function hideCard(card) {

        card.classList.add(hiddenCardClassName);
    }

     function showCard(card) {

        card.classList.remove(hiddenCardClassName);
    }

    function hideAllCards() {

        cards.forEach( ( card ) => {

            if ( !card.classList.contains( matchedCardClassName ) ) {
                hideCard(card);
            }
        });

        selectedCards = [];
    }

    function checkIfMatched() {

        if ( selectedCards.length === 2 ) {

            if( getCardId(selectedCards[0]).some( id => getCardId(selectedCards[1]).includes(id)) && getCardLanguage(selectedCards[0]) !== getCardLanguage(selectedCards[1]) ) {

                selectedCards.forEach( (card) => {

                    card.classList.add(matchedCardClassName);
                });

                selectedCards = [];
            }
        }

        if( checkIfGameIsFinished() ) {

            finishGame();
        }
    }

    function checkIfGameIsFinished() {

        let matchedCards = document.querySelectorAll(".card.matched")

        if( cards.length === matchedCards.length ) {
            return true;
        } else {
            return false;
        }
    }

    function flipCard(card) {

        if ( card.classList.contains( hiddenCardClassName )) {

           if ( selectedCards.length < 2 ) {

               showCard( card );
               selectedCards.push( card );
           }

           if ( selectedCards.length === 2 ) {

             checkIfMatched();
           }
        }
    }

    function getCardId(card) {

        return JSON.parse(card.dataset.id);
    }

    function getCardLanguage(card) {
        return card.dataset.language;
    }

    function getCardIdList() {

        let cardIdList = [];

        cards.forEach( (card) => {

            console.log(getCardId(card));

            cardIdList.push(...getCardId(card));
            console.log(cardIdList);
        });

        return cardIdList;
    }

    function finishGame() {

        const gameSummary = {};

        gameSummary.word_id_list = getCardIdList();

        //Send request to update word practice history
        updatePracticeHistory(gameSummary);
    }

    async function updatePracticeHistory(gameSummary) {

        try {
            const response = await fetch("/update-practice-history", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify( gameSummary )
            });
        } catch (error) {

            console.log(error);
        }
    }

    cards.forEach(card => {
        card.addEventListener("click", function () {
            flipCard(card);
        });
    });

    document.addEventListener('keydown', function(event) {
      if (event.code === 'Space' || event.key === ' ') {

        if ( selectedCards.length === 2 ) {
            hideAllCards();
        }
        event.preventDefault();
      }
    });
});
