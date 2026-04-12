import sys

files = [
    "bcaa.html",
    "creatine.html",
    "eaa.html",
    "gainer.html",
    "pre.html",
    "whey.html"
]

CSS_ADDITION = """
        .stars {
            color: #ff9900;
            font-size: 14px;
            margin: 5px 0;
            letter-spacing: 2px;
        }
        .review-count {
            color: #007185;
            font-size: 12px;
            text-decoration: none;
            margin-left: 5px;
            letter-spacing: normal;
        }
        .modal-reviews-section {
            margin-top: 25px;
            text-align: left;
            border-top: 1px solid #ccc;
            padding-top: 15px;
        }
        .modal-reviews-section h3 {
            margin-top: 0;
            font-size: 18px;
            margin-bottom: 15px;
        }
        .review-item {
            margin-bottom: 15px;
            padding: 10px;
            background: #f9f9f9;
            border-radius: 8px;
            border-bottom: 1px solid #eee;
        }
        .review-user {
            font-weight: bold;
            font-size: 14px;
            margin-bottom: 5px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .review-user .stars {
            margin: 0;
            font-size: 12px;
        }
        .review-text {
            font-size: 13px;
            color: #444;
            line-height: 1.4;
            margin: 0;
        }
        .modal-rating-header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin-bottom: 15px;
        }
        .modal-rating-header .stars {
            font-size: 18px;
        }
    </style>
"""

JS_ADDITION_1 = """

        // --- Reviews Generation Logic ---
        function getStarsHtml(rating) {
            let html = '';
            for (let i = 1; i <= 5; i++) {
                if (i <= rating) html += '★';
                else if (i - 0.5 <= rating) html += '☆'; // Simplification 
                else html += '☆';
            }
            return html;
        }

        document.addEventListener("DOMContentLoaded", () => {
            document.querySelectorAll('.product-card').forEach(card => {
                const rating = (Math.random() * (5 - 4) + 4).toFixed(1);
                const reviews = Math.floor(Math.random() * 500) + 50;
                card.dataset.rating = rating;
                card.dataset.reviews = reviews;

                const infoDiv = card.querySelector('.product-info');
                const priceElement = card.querySelector('.price');
                
                const starsDiv = document.createElement('div');
                starsDiv.className = 'stars';
                starsDiv.innerHTML = getStarsHtml(rating) + `<span class="review-count">(${reviews})</span>`;
                
                infoDiv.insertBefore(starsDiv, priceElement);
            });
        });

        /* --- Modal Logic --- */"""

JS_MODAL_INJECTION = """
            // Find rating for the modal
            let rating = "4.5", reviews = "120";
            document.querySelectorAll('.product-card').forEach(card => {
                if (card.querySelector('h4').innerText === name) {
                    rating = card.dataset.rating || rating;
                    reviews = card.dataset.reviews || reviews;
                }
            });

            document.getElementById("modalRatingStars").innerHTML = getStarsHtml(rating);
            document.getElementById("modalRatingCount").innerText = `${rating} out of 5 (${reviews} global ratings)`;
            
            generateRandomReviews();

            // Set button actions"""

JS_REVIEW_INJECTION = """
        const fakeReviewNames = ["John D.", "Sarah M.", "Alex K.", "Priya S.", "Mike T.", "Emma B."];
        const fakeReviewTexts = [
            "Great product! Delivered on time and tastes amazing.",
            "Mixes really well. Have noticed good results in a few weeks.",
            "A bit expensive, but the quality is definitely there. Highly recommend.",
            "Love the texture and flavor. Will buy again.",
            "Best value for money. Easily digestable and no bloating.",
            "Genuine product. The packaging was top notch."
        ];

        function generateRandomReviews() {
            const container = document.getElementById("modalReviewsList");
            if (!container) return;
            container.innerHTML = "";
            const numReviews = Math.floor(Math.random() * 3) + 2; // 2 to 4 reviews
            
            for (let i = 0; i < numReviews; i++) {
                const name = fakeReviewNames[Math.floor(Math.random() * fakeReviewNames.length)];
                const text = fakeReviewTexts[Math.floor(Math.random() * fakeReviewTexts.length)];
                const rating = (Math.random() * (5 - 4) + 4).toFixed(1);
                
                const reviewDiv = document.createElement("div");
                reviewDiv.className = "review-item";
                reviewDiv.innerHTML = `
                    <div class="review-user">
                        <span>${name}</span>
                        <div class="stars">${getStarsHtml(rating)}</div>
                    </div>
                    <p class="review-text">${text}</p>
                `;
                container.appendChild(reviewDiv);
            }
        }

        function closeModal() {"""


HTML_MODAL_INJECTION = """
            <h2 id="modalName"></h2>
            <div class="modal-rating-header">
                <div class="stars" id="modalRatingStars"></div>
                <span class="review-count" id="modalRatingCount" style="font-size: 14px;"></span>
            </div>
            <p id="modalPrice" class="price"></p>"""

HTML_MODAL_INJECTION_END = """
            <div class="modal-buttons">
                <button id="modalOrderBtn" style="background: #ff9900; border: none; color: black;">Order Now</button>
                <button id="modalCartBtn" style="background: #f0c14b; border: 1px solid #a88734; color: #111;">Add to Cart</button>
            </div>

            <div class="modal-reviews-section">
                <h3>Top Reviews</h3>
                <div id="modalReviewsList"></div>
            </div>
        </div>"""


for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Check if already patched to avoid duplicating
    if "modal-reviews-section" in content:
        print(f"Skipping {f}, already patched.")
        continue

    # 1. Patch CSS
    content = content.replace("    </style>", CSS_ADDITION, 1)

    # 2. Patch JS Generation code
    content = content.replace("        /* --- Modal Logic --- */", JS_ADDITION_1, 1)

    # 3. Patch JS openModal variables
    if "// Set button actions" in content:
        content = content.replace("            // Set button actions", JS_MODAL_INJECTION, 1)

    # 4. Patch JS Reviews function
    content = content.replace("        function closeModal() {", JS_REVIEW_INJECTION, 1)

    # 5. Patch HTML Modal Name & Price
    content = content.replace("""            <h2 id="modalName"></h2>
            <p id="modalPrice" class="price"></p>""", HTML_MODAL_INJECTION, 1)

    # 6. Patch HTML Modal Buttons & Reviews Section
    # BCAA, Creatine, EAA might have "Add to Cart</button> \\n </div> \\n </div>"
    import re
    # Find the end of modal-content div basically where modal-buttons end
    pattern = re.compile(r'            <div class="modal-buttons">.*?</div>\s*</div>', re.DOTALL)
    match = pattern.search(content)
    if match:
        content = content[:match.start()] + HTML_MODAL_INJECTION_END + content[match.end():]

    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
        
    print(f"Patched {f}")
