
// ===== Products Data =====
const productsData = {
    whey: generateProducts("Whey Protein", "whey"),
    creatine: generateProducts("Creatine", "creatine"),
    pre: generateProducts("Pre Workout", "pre"),
    bcaa: generateProducts("BCAA", "bcaa"),
    eaa: generateProducts("EAA", "eaa"),
    gainer: generateProducts("Mass Gainer", "gainer")
};

// ===== Generate 20 products for a category =====
function generateProducts(name, folder) {
    const list = [];
    for (let i = 1; i <= 20; i++) {
        list.push({
            name: `${name} ${i}`,
            price: 1000 + i * 100,
            img: `img/${folder}${i}.jpg`,
            desc: ["High Quality Supplement", "Boost Performance", "Muscle Growth Support"]
        });
    }
    return list;
}

// ===== Display Grid =====
function showGrid(category) {
    const grid = document.getElementById("grid");
    grid.innerHTML = "";
    const products = productsData[category];
    products.forEach((p, i) => {
        const div = document.createElement("div");
        div.className = "product-card";
        div.innerHTML = `<img src="${p.img}" alt="${p.name}"><h4>${p.name}</h4><p>₹${p.price}</p>`;
        div.onclick = () => showDetail(category, i);
        grid.appendChild(div);
    });
    showSection("grid");
}

// ===== Display Product Detail =====
let currentProduct = null;
function showDetail(category, index) {
    currentProduct = productsData[category][index];
    document.getElementById("pimg").src = currentProduct.img;
    document.getElementById("pname").innerText = currentProduct.name;
    document.getElementById("pprice").innerText = "₹" + currentProduct.price;
    const ul = document.getElementById("pdesc");
    ul.innerHTML = "";
    currentProduct.desc.forEach(d => {
        const li = document.createElement("li");
        li.innerText = d;
        ul.appendChild(li);
    });
    showSection("detail");
}

// ===== Show Order Form =====
function showOrder() {
    document.getElementById("oimg").src = currentProduct.img;
    document.getElementById("oname").innerText = currentProduct.name;
    document.getElementById("oprice").innerText = "₹" + currentProduct.price;
    showSection("order");
}

// ===== Submit Order via WhatsApp =====
function orderNow() {
    const name = encodeURIComponent(document.getElementById("name").value.trim());
    const phone = encodeURIComponent(document.getElementById("phone").value.trim());
    const email = encodeURIComponent(document.getElementById("email").value.trim());

    if (!name || !phone || !email) {
        alert("Please fill all fields!");
        return;
    }

    const msg = `Order:%0AProduct: ${encodeURIComponent(currentProduct.name)}%0APrice: ₹${currentProduct.price}%0AName: ${name}%0APhone: ${phone}%0AEmail: ${email}`;
    window.open(`https://api.whatsapp.com/send?phone=917339563621&text=${msg}`, "_blank");
}

// ===== Navigation Sections =====
function showSection(id) {
    ["grid", "detail", "order"].forEach(s => {
        const el = document.getElementById(s);
        if (el) el.style.display = s === id ? "block" : "none";
    });
}

function backToGrid() { showSection("grid"); }
function backToDetail() { showSection("detail"); }