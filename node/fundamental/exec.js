//exec.js
//can execute a command in the terminal inside nodejs
const { execSync } = require("child_process");

// exec("ls -l", (err, stdout, stderr) => {
//   console.log("stdout:", stdout);
//   console.log("stderr:", stderr);
//   console.log("err:", err);
//   if (err) {
//     console.error("Error executing command:", err);
//     return;
//   }
// });
const commitMessage = process.argv[2];
if (!commitMessage) {
  console.error("Please provide a commit message as an argument.");
  process.exit(1);
}
try {
  execSync("git add .");
  execSync(`git commit -m "${commitMessage}"`);
  execSync("git push");
  console.log("Changes pushed to remote repository successfully.");
} catch (error) {
  console.error("Error executing git commands:", error);
}
