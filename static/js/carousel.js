function carousel() {
    return {
        currentIndex: 0,
        offset: 0,
        isDragging: false,
        startX: 0,
        currentX: 0,
        cards: [],
        cardWidth: 0,
        cardHeight: 0,
        containerWidth: 0,
        containerHeight: 0,
        cardRatio: 691 / 1015, // Ratio largeur/hauteur des cartes
        gap: 30,

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

            // Calculer les dimensions du conteneur
            this.containerWidth = this.$refs.wrapper.offsetWidth;
            this.containerHeight = this.$refs.wrapper.offsetHeight;

            // Ajouter une marge pour l'ombre (20px en haut et en bas)
            const shadowMargin = 40; // 20px top + 20px bottom

            // Calculer la hauteur maximale disponible en tenant compte de l'ombre
            const maxHeight = this.containerHeight - shadowMargin;
            const maxWidth = maxHeight * this.cardRatio;

            // Déterminer les dimensions des cartes en respectant le ratio
            if (maxWidth * 2 + this.gap > this.containerWidth) {
                // Si on ne peut pas afficher 2 cartes complètes, on ajuste selon la largeur
                this.cardWidth = Math.min(
                    (this.containerWidth - this.gap * 2) / 2.5,
                    maxWidth
                );
                this.cardHeight = this.cardWidth / this.cardRatio;
            } else {
                // Sinon on utilise la hauteur maximale
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

            // Cloner les cartes au début et à la fin pour l'effet infini
            originalCards.forEach((card) => {
                const cloneBefore = card.cloneNode(true);
                const cloneAfter = card.cloneNode(true);
                cloneBefore.classList.add('clone');
                cloneAfter.classList.add('clone');

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

            // Si on est allé trop loin à droite
            if (this.currentIndex >= totalOriginalCards) {
                this.currentIndex = 0;
                this.offset = -(
                    totalOriginalCards *
                    (this.cardWidth + this.gap)
                );
                this.updatePosition(false);
            }
            // Si on est allé trop loin à gauche
            else if (this.currentIndex < 0) {
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

        // Gestion du drag pour desktop
        handleMouseDown(e) {
            this.isDragging = true;
            this.startX = e.clientX;
            this.$refs.track.style.cursor = 'grabbing';
        },

        handleMouseMove(e) {
            if (!this.isDragging) return;
            e.preventDefault();
            const x = e.clientX;
            const walk = x - this.startX;
            this.$refs.track.style.transform = `translateX(${
                this.offset + walk
            }px)`;
        },

        handleMouseUp(e) {
            if (!this.isDragging) return;
            this.isDragging = false;
            this.$refs.track.style.cursor = 'grab';

            const walk = e.clientX - this.startX;
            if (Math.abs(walk) > 100) {
                if (walk > 0) {
                    this.prev();
                } else {
                    this.next();
                }
            } else {
                this.updatePosition(true);
            }
        },

        // Gestion du touch pour mobile
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
