export function get_random_id() {
  return Math.floor(Math.random() * 0x10000 + 0x10);
}

export function reload(from) {
  alert(`Server Error frpm ${from}... Reload`);
  //location.href = "/";
}
