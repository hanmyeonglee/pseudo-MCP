export function get_random_id(): number {
    return Math.floor(Math.random() * 0x10000 + 0x10);
}