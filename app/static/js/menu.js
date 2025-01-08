var storage = [];

const productsContainer = document.querySelector(
   ".app__container-products__menu"
);
const orderContainer = document.querySelector(".app__container-order__list");

function AddToCart(btn, product) {
   const selectImgDiv =
      btn.parentElement.parentElement.querySelector("picture img");
   selectImgDiv.classList.add("selected");
   const quantityDiv = btn.nextElementSibling;
   quantityDiv.classList.add("show");
   btn.classList.add("hide");
   addOrder(product);
   renderOrders();
}

function increment(product, quantity) {
   let quantityVal = quantity.parentElement.querySelector("span");
   const findProduct = findProductById(product.id);
   findProduct.find.quantity += 1;
   findProduct.find.totalPrice += findProduct.find.price;
   quantityVal.innerText = findProduct.find.quantity;
   updateStorage(findProduct.orderList);
   renderOrders();
}
function decrement(product, quantity) {
   let quantityVal = quantity.parentElement.querySelector("span");
   const findProduct = findProductById(product.id);
   if (findProduct.find.quantity <= 1) {
      removeOrder(product.id);
      return;
   }
   findProduct.find.quantity -= 1;
   findProduct.find.totalPrice -= findProduct.find.price;
   updateStorage(findProduct.orderList);
   quantityVal.innerText = findProduct.find.quantity;
   renderOrders();
}

function addOrder(order) {
   let orderDetails = {
      id: order.id,
      name: order.name,
      price: order.price,
   };
   const findOrder = findProductById(orderDetails.id);
   if (findOrder.find) {
      findOrder.find.quantity += 1;
      findOrder.find.totalPrice += orderDetails.price;
   } else {
      orderDetails.quantity = 1;
      orderDetails.totalPrice = orderDetails.price;
      findOrder.orderList.push(orderDetails);
   }
   updateStorage(findOrder.orderList);
}

function removeOrder(orderId) {
   const quantityBtn = document.querySelectorAll(
      ".product__container-image .product__actions .quantity"
   );
   const parseCurrentOrder = findProductById(orderId);
   let targetOrderIndex = parseCurrentOrder.orderList.findIndex(
      (e) => e.id == +orderId
   );
   if (targetOrderIndex > -1) {
      parseCurrentOrder.orderList.splice(targetOrderIndex, 1);
   }

   Array.from(quantityBtn, (e) => {
      let cartBtn = e.previousElementSibling;
      let qValue = e.querySelector("span");
      let selectedImg =
         e.parentElement.parentElement.querySelector("picture img");
      if (+cartBtn.id === +orderId) {
         qValue.innerText = 1;
         e.classList.remove("show");
         cartBtn.classList.remove("hide");
         selectedImg.classList.remove("selected");
      }
   });
   updateStorage(parseCurrentOrder.orderList);
   renderOrders();
}

function renderOrders() {
   const orderCounter = document.querySelector(".app__container-order h1 span");
   let totalPrice = 0;
   let totalQuantity = 0;
   const currentOrders = storage
   if (currentOrders.length < 1) {
      orderContainer.innerHTML = `
    <div class='app__container-order__list-empty'>
    <img src='/fos/static/images/menu/illustration-empty-cart.svg'>
    <span>Your added items will appear here</span>
    </div>
    `;
   } else {
      orderContainer.innerHTML = "";
      currentOrders.map((order) => {
         totalPrice += order.totalPrice;
         totalQuantity += order.quantity;
         orderContainer.innerHTML += `
        <div class='order-box'>
        <h2>${order.name}</h2>
        <div class='orderDetails'>
        <span>${order.quantity}</span>
        <span>@ $${order.price.toFixed(2)}</span>
        <span>$${order.totalPrice.toFixed(2)}</span>
        </div>
        <img src= '/fos/static/images/menu/icon-remove-item.svg' id='${
           order.id
        }' onclick='removeOrder(this.id)'>
        </div>
        `;
      });
   }
   orderCounter.innerText = totalQuantity;
   renderOrdersDetails(currentOrders, totalPrice);
}

function renderOrdersDetails(orders, totalPrice) {
   const totalOrdersContainer = document.querySelector(
      ".app__container-order__total"
   );
   const infoContainer = document.querySelector(".app__container-order__info");
   const orderBtn = document.querySelector(".app__container-order__btn");
   const totalElement = document.querySelector(".total");
   if (orders.length < 1) {
      totalOrdersContainer.style.display = "none";
      infoContainer.style.display = "none";
      orderBtn.style.display = "none";
   } else {
      totalOrdersContainer.style.display = "flex";
      infoContainer.style.display = "flex";
      orderBtn.style.display = "block";
   }
   totalElement.textContent = `$${totalPrice.toFixed(2)}`;
}

function findProductById(id = "") {
   return {
      orderList: storage,
      find: storage.find((product) => product.id === id),
   };
}

function updateStorage(data) {
   storage = data;
   reduced_data = []
   for (let i=0; i < data.length; i++) {
      reduced_data.push({
         "id": data[i].id,
         "quantity": data[i].quantity,
      });
   }
   document.getElementById("order").value = JSON.stringify(reduced_data);
}

function showCart() {
   const cart = document.querySelector(".app__container-order");
   cart.classList.toggle("show__app__container-order");
}
function hideCart() {
   const cart = document.querySelector(".app__container-order");
   cart.classList.remove("show__app__container-order");
}

// modal

function closeModal() {
   const modalOverlay = document.querySelector('.modal-overlay.show');
   modalOverlay.classList.remove("show");
}

renderOrders();
