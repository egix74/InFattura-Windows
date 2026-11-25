using System;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;
class LauncherPortatile {
  [STAThread] static void Main() {
    try {
      string dir = AppDomain.CurrentDomain.BaseDirectory;
      string python = Path.Combine(dir, "runtime", "pythonw.exe");
      string app = Path.Combine(dir, "app.py");
      if (!File.Exists(python) || !File.Exists(app)) {
        MessageBox.Show("Estrai tutti i file dello ZIP e conserva l'eseguibile insieme alla cartella runtime e ai file dell'app.", "InFattura", MessageBoxButtons.OK, MessageBoxIcon.Warning);
        return;
      }
      Process.Start(new ProcessStartInfo(python, "-E -s \"" + app + "\"") { UseShellExecute = false, WorkingDirectory = dir, CreateNoWindow = true });
    } catch (Exception e) {
      MessageBox.Show("Impossibile avviare InFattura: " + e.Message, "InFattura", MessageBoxButtons.OK, MessageBoxIcon.Error);
    }
  }
}
