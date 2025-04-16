const { exec } = require('child_process');

const file = process.env.FUNCTION_FILE || 'hello.js';
let args = [];

try {
  args = JSON.parse(process.env.ARGS || '[]');
} catch (e) {
  console.error('Failed to parse ARGS:', e);
}

const command = `node /functions/${file} ${args.join(' ')}`;

exec(command, (err, stdout, stderr) => {
  if (err) {
    console.error('Execution error:', err);
    console.error(stderr);
    return;
  }
  console.log(stdout);
});
