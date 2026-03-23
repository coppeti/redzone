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
        gap: 35,
        flippedCards: [],
        // Swipe libre :
        isDragging: false,
        dragOffset: 0,
        startX: 0,

        init() {
            this.setupCarousel();
            this.cloneCards();
            this.centerInitial();

            window.addEventListener('resize', () => {
                this.setupCarousel();
                this.centerInitial();
            });
        },

        setupCarousel() {
            const container = this.$refs.track;
            const cards = container.querySelectorAll('.card:not(.clone)');
            this.cards = Array.from(cards);

            if (this.flippedCards.length !== this.cards.length) {
                this.flippedCards = new Array(this.cards.length).fill(false);
            }

            // 1. Dimensions du wrapper à disposition
            this.containerWidth = this.$refs.wrapper.offsetWidth;
            // Hauteur disponible viewport - header (196) - footer (30)
            const headerHeight = 196;
            const footerHeight = 30;
            const usableHeight =
                window.innerHeight - headerHeight - footerHeight;
            const maxCardHeight = 1000;
            const maxCardWidth = 681;
            const cardRatio = this.cardRatio;

            // 2. On veut la carte la plus haute possible, mais sans dépasser 1000px ni rognée en largeur
            let targetHeight = Math.min(usableHeight, 1000);
            let targetWidth = targetHeight * this.cardRatio;

            if (targetWidth > this.containerWidth) {
                targetWidth = this.containerWidth;
                targetHeight = targetWidth / this.cardRatio;
            } else {
                // Sinon, on ne dépasse pas la largeur maximale, donc OK
                targetWidth = Math.min(targetWidth, maxCardWidth);
                targetHeight = targetWidth / cardRatio;
            }

            this.cardWidth = targetWidth;
            this.cardHeight = targetHeight;

            // GAP dynamique ou fixe selon tes goûts
            this.gap = window.innerWidth <= 768 ? 8 : 30;
            this.cardTotalWidth = this.cardWidth + this.gap;

            // Applique styles width/height aux cartes du DOM
            const allCards = container.querySelectorAll('.card');
            allCards.forEach((card) => {
                card.style.width = `${this.cardWidth}px`;
                card.style.height = `${this.cardHeight}px`;
            });

            // Centrage horizontal (première carte au centre du viewport)
            this.offset = (this.containerWidth - this.cardWidth) / 2;
            this.updatePosition(false);
        },

        cloneCards() {
            const track = this.$refs.track;
            Array.from(track.querySelectorAll('.clone')).forEach((c) =>
                c.remove()
            );

            const originalCards = Array.from(
                track.querySelectorAll('.card:not(.clone)')
            );

            // Clonage APRES (ordre "normal")
            originalCards.forEach((card, index) => {
                const cloneAfter = card.cloneNode(true);
                cloneAfter.classList.add('clone');
                cloneAfter.setAttribute('data-clone-index', index);
                track.appendChild(cloneAfter);
            });
            // Clonage AVANT (ordre inversé pour sens rewind)
            originalCards
                .slice()
                .reverse()
                .forEach((card, index) => {
                    const cloneBefore = card.cloneNode(true);
                    cloneBefore.classList.add('clone');
                    // Option : index inversé ou non, ici pour debug/traçage c'est le même
                    cloneBefore.setAttribute('data-clone-index', index);
                    track.insertBefore(cloneBefore, track.firstChild);
                });
        },

        centerInitial() {
            // On cible la première vraie carte (après les clones)
            const allCards = this.$refs.track.querySelectorAll('.card');
            const firstRealCardIndex = this.cards.length;

            // Position (en px) du bord gauche de la première vraie carte dans le track
            let cardRect = allCards[firstRealCardIndex].getBoundingClientRect();
            let trackRect = this.$refs.track.getBoundingClientRect();
            let wrapperRect = this.$refs.wrapper.getBoundingClientRect();

            // Offset du début de la vraie carte PAR RAPPORT AU TRACK
            let leftInTrack = allCards[firstRealCardIndex].offsetLeft;

            // Pour centrer cette carte dans le wrapper :
            this.offset =
                this.containerWidth / 2 - (leftInTrack + this.cardWidth / 2);

            this.updatePosition(false);
        },

        normalizeForInfinite() {
            // Nombre de vraies cartes
            const cardCount = this.cards.length;
            const trackLength = cardCount * this.cardTotalWidth;

            // Valeur min = tout le track original + 1, à gauche (on a N clones devant)
            // Valeur max = -clones devant, à droite (car on a N clones après)
            const minOffset =
                (this.containerWidth - this.cardWidth) / 2 - trackLength * 2;
            const maxOffset = (this.containerWidth - this.cardWidth) / 2;

            if (this.offset > maxOffset) {
                // Si on est allé trop à droite ("avant" les clones), on recentre sur le set du milieu
                this.offset = this.offset - trackLength;
            } else if (this.offset < minOffset) {
                // Si on est allé trop à gauche ("après" tous les clones), on recentre sur le set du milieu
                this.offset = this.offset + trackLength;
            }
            this.updatePosition(false);
        },

        updatePosition(animate) {
            const track = this.$refs.track;
            if (animate) {
                track.style.transition =
                    'transform 0.5s cubic-bezier(0.4,0,0.2,1)';
            } else {
                track.style.transition = 'none';
            }
            track.style.transform = `translateX(${this.offset}px)`;
        },

        // === SWIPE LIBRE MOBILE/DESKTOP ===

        handleTouchStart(e) {
            this.startX = e.touches ? e.touches[0].clientX : e.clientX;
            this.isDragging = true;
            this.dragOffset = this.offset;
        },

        handleTouchMove(e) {
            if (!this.isDragging) return;
            const x = e.touches ? e.touches[0].clientX : e.clientX;
            const walk = x - this.startX;
            this.offset = this.dragOffset + walk;
            this.updatePosition(false);
        },

        handleTouchEnd(e) {
            this.isDragging = false;
            // Boucle infini
            setTimeout(() => this.normalizeForInfinite(), 10);
        },

        handleMouseDown(e) {
            e.preventDefault();
            this.isDragging = true;
            this.startX = e.clientX;
            this.dragOffset = this.offset;
            document.addEventListener(
                'mousemove',
                (this.boundMouseMove = this.handleMouseMove.bind(this))
            );
            document.addEventListener(
                'mouseup',
                (this.boundMouseUp = this.handleMouseUp.bind(this))
            );
        },

        handleMouseMove(e) {
            if (!this.isDragging) return;
            const x = e.clientX;
            const walk = x - this.startX;
            this.offset = this.dragOffset + walk;
            this.updatePosition(false);
        },

        handleMouseUp(e) {
            this.isDragging = false;
            setTimeout(() => this.normalizeForInfinite(), 10);
            document.removeEventListener('mousemove', this.boundMouseMove);
            document.removeEventListener('mouseup', this.boundMouseUp);
        },

        // ==== flipping gestion ====
        flipCard(index, $event) {
            const cardInner = $event.target.closest('.card-inner');
            if (cardInner.classList.contains('flipping')) return;

            cardInner.classList.add('flipping');
            this.flippedCards[index] = !this.flippedCards[index];
            setTimeout(() => {
                cardInner.classList.remove('flipping');
            }, 600);
        },

        isCardFlipped(index) {
            return this.flippedCards[index] || false;
        },

        move(direction) {
            const allCards = this.$refs.track.querySelectorAll('.card');
            const totalCards = allCards.length;
            const carouselCenter = this.containerWidth / 2;

            let bestIndex = 0;
            let bestDelta = Infinity;
            for (let i = 0; i < totalCards; i++) {
                const cardCenter = allCards[i].offsetLeft + this.offset + this.cardWidth / 2;
                const delta = Math.abs(carouselCenter - cardCenter);
                if (delta < bestDelta) {
                    bestDelta = delta;
                    bestIndex = i;
                }
            }

            let targetIndex = bestIndex + direction;
            if (targetIndex >= totalCards) targetIndex = 0;
            if (targetIndex < 0) targetIndex = totalCards - 1;

            const targetCard = allCards[targetIndex];
            this.offset = carouselCenter - (targetCard.offsetLeft + this.cardWidth / 2);
            this.updatePosition(true);

            setTimeout(() => this.normalizeForInfinite(), 520);
        },

        next() { this.move(1); },
        prev() { this.move(-1); },
    };


}
