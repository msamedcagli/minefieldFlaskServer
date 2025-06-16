const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const CELL_SIZE = 40;
const GRID_SIZE = 10;

canvas.addEventListener("contextmenu", e => e.preventDefault());

canvas.addEventListener("mousedown", (e) => {
  const rect = canvas.getBoundingClientRect();
  const x = Math.floor((e.clientX - rect.left) / CELL_SIZE);
  const y = Math.floor((e.clientY - rect.top) / CELL_SIZE);

  const endpoint = e.button === 2 ? "/flag" : "/click";
  fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ x, y })
  }).then(() => update());
});

function draw(state) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const { grid, revealed, flags, game_over, won } = state;

  for (let y = 0; y < GRID_SIZE; y++) {
    for (let x = 0; x < GRID_SIZE; x++) {
      const px = x * CELL_SIZE;
      const py = y * CELL_SIZE;

      ctx.strokeStyle = "#333";
      ctx.strokeRect(px, py, CELL_SIZE, CELL_SIZE);

      if (revealed[y][x]) {
        ctx.fillStyle = "#eee";
        ctx.fillRect(px, py, CELL_SIZE, CELL_SIZE);
        if (grid[y][x] > 0) {
          ctx.fillStyle = "black";
          ctx.fillText(grid[y][x], px + 15, py + 25);
        } else if (grid[y][x] === -1) {
          ctx.fillStyle = "red";
          ctx.beginPath();
          ctx.arc(px + 20, py + 20, 10, 0, 2 * Math.PI);
          ctx.fill();
        }
      } else {
        ctx.fillStyle = "#999";
        ctx.fillRect(px, py, CELL_SIZE, CELL_SIZE);
        if (flags[y][x]) {
          ctx.fillStyle = "blue";
          ctx.fillText("⚑", px + 10, py + 30);
        }
      }
    }
  }

  const status = document.getElementById("status");
  const gameOverMessage = document.getElementById("gameOverMessage");
  
  if (game_over) {
    status.textContent = "💥 OYUN BİTTİ!";
    gameOverMessage.textContent = "💥 OYUN BİTTİ!";
    gameOverMessage.style.display = "block";
  } else if (won) {
    status.textContent = "🎉 KAZANDIN!";
    gameOverMessage.textContent = "🎉 TEBRİKLER! KAZANDIN!";
    gameOverMessage.style.display = "block";
  } else {
    status.textContent = "Oyun devam ediyor...";
    gameOverMessage.style.display = "none";
  }
}
document.getElementById("resetBtn").addEventListener("click", () => {
  fetch("/reset", { method: "POST" })
    .then(() => update());
});


function update() {
  fetch("/state")
    .then(res => res.json())
    .then(draw);
}

update();
setInterval(update, 1000);
