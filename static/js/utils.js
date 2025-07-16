export function showError(id, msg) {
  const el = document.getElementById(id);
  if (el) {
    el.innerText = msg;
    el.style.display = "block";
  }
}

export function clearErrors(id) {
  const el = document.getElementById(id);
  if (el) el.innerText = "";
}