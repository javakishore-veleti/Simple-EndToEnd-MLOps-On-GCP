
const { execSync } = require('child_process');

const filePath = process.argv[2];
if (!filePath) {
  console.error('❌ Please provide a file path as an argument.');
  process.exit(1);
}

const bucketName = 'gs://e2e-ml-ops/';
console.log(`Uploading ${filePath} to ${bucketName}...`);

execSync(`gsutil cp "${filePath}" ${bucketName}`, { stdio: 'inherit' });
