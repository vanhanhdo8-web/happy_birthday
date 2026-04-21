// Chạy: node generate-all-images.js từ thư mục style/
// Tạo images.json chứa TẤT CẢ .jpg files

const fs = require('fs');
const path = require('path');

const imgDir = path.join(__dirname, 'img');
const exts = ['.jpg', '.jpeg'];

let files = [];
try {
  files = fs.readdirSync(imgDir)
    .filter(f => exts.includes(path.extname(f).toLowerCase()))
    .sort((a, b) => a.localeCompare(b));
} catch (err) {
  console.error('❌ Không tìm thấy thư mục img:', err.message);
  process.exit(1);
}

fs.writeFileSync(
  path.join(imgDir, 'images.json'),
  JSON.stringify(files, null, 2)
);

console.log(`✅ Tìm thấy ${files.length} ảnh JPG, đã lưu vào ./img/images.json`);
console.log('Files:');
files.forEach(f => console.log(' -', f));

