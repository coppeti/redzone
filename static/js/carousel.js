function carousel() {
    return {
        currentIndex: 0,
        offset: 0,
        cards: [],
        cardWidth: 0,
        cardHeight: 0,
        containerWidth: 0,
        containerHeight: 0,
        cardRatio: 681 / 1000,
        gap: 30,
        flippedCards: [], // Pour suivre les cartes retournées

        init() {
            this.setupCarousel();
            this.cloneCards();

            window.addEventListener('resize', () => {
                this.setupCarousel();
            });
        },

        setupCarousel() {
            const container = this.$refs.track;
            const cards = container.querySelectorAll('.card:not(.clone)');
            this.cards = Array.from(cards);

            // Initialiser le tableau des cartes retournées
            this.flippedCards = new Array(this.cards.length).fill(false);

            // Calculer les dimensions du conteneur
            this.containerWidth = this.$refs.wrapper.offsetWidth;
            this.containerHeight = this.$refs.wrapper.offsetHeight;

            // Ajouter une marge pour l'ombre (20px en haut et en bas)
            const shadowMargin = 40;

            // Calculer la hauteur maximale disponible en tenant compte de l'ombre
            const maxHeight = this.containerHeight - shadowMargin;
            const maxWidth = maxHeight * this.cardRatio;

            // Déterminer les dimensions des cartes en respectant le ratio
            if (maxWidth * 2 + this.gap > this.containerWidth) {
                this.cardWidth = Math.min(
                    (this.containerWidth - this.gap * 2) / 2.5,
                    maxWidth
                );
                this.cardHeight = this.cardWidth / this.cardRatio;
            } else {
                this.cardHeight = maxHeight;
                this.cardWidth = this.cardHeight * this.cardRatio;
            }

            // Appliquer les dimensions aux cartes
            const allCards = container.querySelectorAll('.card');
            allCards.forEach((card) => {
                card.style.width = `${this.cardWidth}px`;
                card.style.height = `${this.cardHeight}px`;
            });

            // Position initiale au centre des cartes clonées
            this.offset = -(this.cards.length * (this.cardWidth + this.gap));
            this.updatePosition(false);
        },

        cloneCards() {
            const track = this.$refs.track;
            const originalCards = Array.from(track.querySelectorAll('.card'));

            originalCards.forEach((card, index) => {
                const cloneBefore = card.cloneNode(true);
                const cloneAfter = card.cloneNode(true);
                cloneBefore.classList.add('clone');
                cloneAfter.classList.add('clone');

                // Marquer les clones avec un attribut data
                cloneBefore.setAttribute('data-clone-index', index);
                cloneAfter.setAttribute('data-clone-index', index);

                track.insertBefore(cloneBefore, track.firstChild);
                track.appendChild(cloneAfter);
            });
        },

        next() {
            this.currentIndex++;
            this.offset -= this.cardWidth + this.gap;
            this.updatePosition(true);

            setTimeout(() => {
                this.checkInfiniteScroll();
            }, 500);
        },

        prev() {
            this.currentIndex--;
            this.offset += this.cardWidth + this.gap;
            this.updatePosition(true);

            setTimeout(() => {
                this.checkInfiniteScroll();
            }, 500);
        },

        checkInfiniteScroll() {
            const totalOriginalCards = this.cards.length;
            const totalWidth = totalOriginalCards * (this.cardWidth + this.gap);

            if (this.currentIndex >= totalOriginalCards) {
                this.currentIndex = 0;
                this.offset = -(
                    totalOriginalCards *
                    (this.cardWidth + this.gap)
                );
                this.updatePosition(false);
            } else if (this.currentIndex < 0) {
                this.currentIndex = totalOriginalCards - 1;
                this.offset = -(
                    (totalOriginalCards * 2 - 1) *
                    (this.cardWidth + this.gap)
                );
                this.updatePosition(false);
            }
        },

        updatePosition(animate) {
            const track = this.$refs.track;
            if (animate) {
                track.style.transition =
                    'transform 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
            } else {
                track.style.transition = 'none';
            }
            track.style.transform = `translateX(${this.offset}px)`;
        },

        // Fonction pour retourner une carte
        flipCard(index) {
            // Empêcher le clic pendant l'animation
            if (
                event.target
                    .closest('.card-inner')
                    .classList.contains('flipping')
            )
                return;

            const cardInner = event.target.closest('.card-inner');
            cardInner.classList.add('flipping');

            // Retourner la carte
            this.flippedCards[index] = !this.flippedCards[index];

            // Retirer la classe flipping après l'animation
            setTimeout(() => {
                cardInner.classList.remove('flipping');
            }, 600);
        },

        isCardFlipped(index) {
            return this.flippedCards[index] || false;
        },

        // Gestion du touch pour mobile uniquement
        handleTouchStart(e) {
            this.startX = e.touches[0].clientX;
        },

        handleTouchMove(e) {
            const x = e.touches[0].clientX;
            const walk = x - this.startX;
            this.$refs.track.style.transform = `translateX(${
                this.offset + walk
            }px)`;
        },

        handleTouchEnd(e) {
            const walk = e.changedTouches[0].clientX - this.startX;
            if (Math.abs(walk) > 50) {
                if (walk > 0) {
                    this.prev();
                } else {
                    this.next();
                }
            } else {
                this.updatePosition(true);
            }
        },
    };
}
