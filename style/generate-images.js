// Chạy lệnh: node generate-images.js
// Tự động quét thư mục ./img và tạo file ./img/images.json

const fs = require('fs');
const path = require('path');

const imgDir = path.join(__dirname, 'img');
const exts = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];

const files = fs.readdirSync(imgDir)
    .filter(f => exts.includes(path.extname(f).toLowerCase()))
    .sort();

fs.writeFileSync(
    path.join(imgDir, 'images.json'),
    JSON.stringify(files, null, 2)
);

console.log(`✅ Tìm thấy ${files.length} ảnh, đã lưu vào ./img/images.json`);
files.forEach(f => console.log(' -', f));