import * as vscode from "vscode";
import { uploadFiles, uploadFolders, saveFile } from "./filePicker";
import { setupVenv, runScript } from "./pythonRunner";

export async function generateUML(
  context: vscode.ExtensionContext,
  useFolders: boolean,
) {
  try {
    const venvPython = await setupVenv(context.extensionUri);
    vscode.window.showInformationMessage("Launching UML generator...");

    const paths = useFolders ? await uploadFolders() : await uploadFiles();
    if (!paths || paths.length === 0) {
      vscode.window.showWarningMessage("No files or folders were selected.");
      return;
    }

    const outputPath = await saveFile();
    if (!outputPath) {
      vscode.window.showWarningMessage("No output file was selected.");
      return;
    }

    const args = ["-o", outputPath, "-p", ...paths];
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
  } catch (error) {
    vscode.window.showErrorMessage(
      `Error: ${error instanceof Error ? error.message : String(error)}`,
    );
  }
}
