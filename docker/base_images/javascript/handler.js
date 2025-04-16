const { exec } = require('child_process');

const file = process.env.FUNCTION_FILE || 'hello.js';
exec(`node /functions/${file}`, (err, stdout, stderr) => {
    if (err) {
        console.error('Execution error:', err);
        return;
    }
    console.log(stdout);
});
