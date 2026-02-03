import { execFile } from "child_process";
import { promisify } from "util";
import { Uri } from "vscode";
import * as fs from "fs";
import * as path from "path";

const execFileAsync = promisify(execFile);

export async function setupVenv(extensionUri: Uri): Promise<string> {
  const venvPath = Uri.joinPath(extensionUri, "venv").fsPath;
  const pythonExe =
    process.platform === "win32"
      ? path.join(venvPath, "Scripts", "python.exe")
      : path.join(venvPath, "bin", "python");

  if (fs.existsSync(pythonExe)) {
    return pythonExe;
  }

  console.log(`Creating virtual environment at ${venvPath}`);
  await execFileAsync("python", ["-m", "venv", venvPath]);

  const reqPath = Uri.joinPath(extensionUri, "requirements.txt").fsPath;
  if (fs.existsSync(reqPath)) {
    console.log("Installing dependencies...");
    await execFileAsync(pythonExe, ["-m", "pip", "install", "-r", reqPath]);
  }

  return pythonExe;
}

export async function runScript(
  pythonExec: string,
  pythonDir: Uri,
  args: string[],
): Promise<string> {
  const scriptPath = Uri.joinPath(pythonDir, "main.py").fsPath;
  try {
    const { stdout } = await execFileAsync(pythonExec, [scriptPath, ...args]);
    return stdout;
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    throw new Error(`Python script failed: ${errorMessage}`);
  }
}
