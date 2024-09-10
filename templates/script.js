// document.addEventListener("DOMContentLoaded", () => {
//   // Create and insert the speed control input into the body
//   const body = document.body;

//   const speedLabel = document.createElement("label");
//   speedLabel.setAttribute("for", "speed-control");
//   speedLabel.textContent = "Speed (seconds):";

//   const speedControl = document.createElement("input");
//   speedControl.setAttribute("type", "number");
//   speedControl.setAttribute("id", "speed-control");
//   speedControl.setAttribute("value", "30"); // Default speed
//   speedControl.setAttribute("min", "10");
//   speedControl.setAttribute("step", "1");

//   // Append label and input to the body
//   body.appendChild(speedLabel);
//   body.appendChild(speedControl);

//   function updateTicker(data) {
//     const container = document.getElementById("ticker-container");
//     container.innerHTML = ""; // Clear previous items

//     data.forEach((item) => {
//       const div = document.createElement("div");
//       div.className = "ticker-item";

//       const arrowClass =
//         item.price_change >= 0 ? "arrow positive" : "arrow negative";
//       const changeClass =
//         item.price_change >= 0 ? "change positive" : "change negative";

//       div.innerHTML = `
//         <img src="logo.png" alt="Logo" class="logo" />
//         <span class="name">${item.name}</span>
//         <span class="price">${item.price}</span>
//         <span class="change ${changeClass}">${item.price_change} (${
//         item.percentage_change
//       }%)</span>
//         <span class="${arrowClass}">${item.price_change >= 0 ? "▲" : "▼"}</span>
//       `;

//       container.appendChild(div);
//     });

//     // Adjust animation duration based on the speed input value
//     updateTickerSpeed();
//   }

//   async function fetchTickerData() {
//     try {
//       const response = await fetch("/api/ticker");
//       const data = await response.json();
//       updateTicker(data);
//     } catch (error) {
//       console.error("Error fetching ticker data:", error);
//     }
//   }

//   function updateTickerSpeed() {
//     const speed = speedControl.value || 30; // Default speed if input is empty
//     const ticker = document.querySelector(".ticker");
//     const totalWidth = ticker.scrollWidth;

//     // Calculate animation duration based on ticker width and speed
//     ticker.style.animationDuration = `${
//       (totalWidth / window.innerWidth) * speed
//     }s`;
//   }

//   // Fetch data every 6 seconds
//   setInterval(fetchTickerData, 6000);
//   // Initial fetch
//   fetchTickerData();

//   // Update ticker speed on input change
//   speedControl.addEventListener("input", updateTickerSpeed);

//   // Set initial speed
//   updateTickerSpeed();
// });
