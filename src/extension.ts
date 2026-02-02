// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from "vscode";
import { uploadFiles, saveFile } from "./file_picker";
import { runScript } from "./python_runner";
import { setupVenv } from "./python_runner";

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
  // Use the console to output diagnostic information (console.log) and errors (console.error)
  // This line of code will only be executed once when your extension is activated
  console.log('Congratulations, your extension "python2uml" is now active!');

  // The command has been defined in the package.json file
  // Now provide the implementation of the command with registerCommand
  // The commandId parameter must match the command field in package.json
  const disposable = vscode.commands.registerCommand(
    "python2uml.generateUML",
    async () => {
      try {
        const venvPython = await setupVenv(context.extensionUri);
        vscode.window.showInformationMessage("Launching UML generator...");

        const filePaths = await uploadFiles();
        const outputPath = await saveFile();

        if (!filePaths || filePaths.length === 0 || !outputPath) {
          vscode.window.showWarningMessage("No files were selected.");
        } else {
          const args = ["-o", outputPath, "-p", ...filePaths];
          const pythonDir = vscode.Uri.joinPath(
            context.extensionUri,
            "src",
            "python",
          );

          try {
            const output = await runScript(venvPython, pythonDir, args);
            console.log(output);
            vscode.window.showInformationMessage(
              "UML diagram generated successfully!",
            );
          } catch (error) {
            vscode.window.showErrorMessage(
              `Error: ${error instanceof Error ? error.message : String(error)}`,
            );
          }
        }
      } catch (error) {
        vscode.window.showErrorMessage(
          `Error: ${error instanceof Error ? error.message : String(error)}`,
        );
      }
    },
  );

  context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
export function deactivate() {}
