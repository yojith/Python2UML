// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from "vscode";
import { uploadFiles, saveFile } from "./filePicker";
import { runScript } from "./pythonRunner";
import { setupVenv } from "./pythonRunner";
import { generateUML } from "./umlGenerator";

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
  // Use the console to output diagnostic information (console.log) and errors (console.error)
  // This line of code will only be executed once when your extension is activated
  console.log('Congratulations, your extension "python2uml" is now active!');

  // The command has been defined in the package.json file
  // Now provide the implementation of the command with registerCommand
  // The commandId parameter must match the command field in package.json
  const commandGenerateUMLFromFiles = vscode.commands.registerCommand(
    "python2uml.generateUMLFromFiles",
    () => {
      generateUML(context, false);
    },
  );

  const commandGenerateUMLFromFolders = vscode.commands.registerCommand(
    "python2uml.generateUMLFromFolders",
    () => {
      generateUML(context, true);
    },
  );

  context.subscriptions.push(commandGenerateUMLFromFiles);
  context.subscriptions.push(commandGenerateUMLFromFolders);
}

// This method is called when your extension is deactivated
export function deactivate() {}
