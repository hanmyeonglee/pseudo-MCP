export function get_random_id() {
  return Math.floor(Math.random() * 0x10000 + 0x10);
}

export function reload() {
  alert(`Server Error... Reload Plz.`);
  //location.href = "/";
}
