const a = parseFloat(process.argv[2]);
const b = parseFloat(process.argv[3]);

if (isNaN(a) || isNaN(b)) {
    console.log("Usage: node arithmetic.js <num1> <num2>");
} else {
    console.log(`Sum: ${a + b}`);
}
