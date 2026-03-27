<div align="center">

# 🎉 Congratulations AbdulRaheemShariff! 🎉

<img src="https://octodex.github.com/images/welcometocat.png" height="200px" />

### 🌟 You've successfully completed the exercise! 🌟

## 🚀 Share Your Success!

**Show off your new skills and inspire others!**

<a href="https://twitter.com/intent/tweet?text=I%20just%20completed%20the%20%22Getting%20Started%20with%20GitHub%20Copilot%22%20GitHub%20Skills%20hands-on%20exercise!%20%F0%9F%8E%89%0A%0Ahttps%3A%2F%2Fgithub.com%2FAbdulRaheemShariff%2Fskills-getting-started1-with-github-copilot%0A%0A%23GitHubSkills%20%23OpenSource%20%23GitHubLearn" target="_blank" rel="noopener noreferrer">
  <img src="https://img.shields.io/badge/Share%20on%20X-1da1f2?style=for-the-badge&logo=x&logoColor=white" alt="Share on X" />
</a>
<a href="https://bsky.app/intent/compose?text=I%20just%20completed%20the%20%22Getting%20Started%20with%20GitHub%20Copilot%22%20GitHub%20Skills%20hands-on%20exercise!%20%F0%9F%8E%89%0A%0Ahttps%3A%2F%2Fgithub.com%2FAbdulRaheemShariff%2Fskills-getting-started1-with-github-copilot%0A%0A%23GitHubSkills%20%23OpenSource%20%23GitHubLearn" target="_blank" rel="noopener noreferrer">
  <img src="https://img.shields.io/badge/Share%20on%20Bluesky-0085ff?style=for-the-badge&logo=bluesky&logoColor=white" alt="Share on Bluesky" />
</a>
<a href="https://www.linkedin.com/feed/?shareActive=true&text=I%20just%20completed%20the%20%22Getting%20Started%20with%20GitHub%20Copilot%22%20GitHub%20Skills%20hands-on%20exercise!%20%F0%9F%8E%89%0A%0Ahttps%3A%2F%2Fgithub.com%2FAbdulRaheemShariff%2Fskills-getting-started1-with-github-copilot%0A%0A%23GitHubSkills%20%23OpenSource%20%23GitHubLearn" target="_blank" rel="noopener noreferrer">
  <img src="https://img.shields.io/badge/Share%20on%20LinkedIn-0077b5?style=for-the-badge&logo=linkedin&logoColor=white" alt="Share on LinkedIn" />
</a>

### 🎯 What's Next?

**Keep the momentum going!**

[![](https://img.shields.io/badge/Return%20to%20Exercise-%E2%86%92-1f883d?style=for-the-badge&logo=github&labelColor=197935)](https://github.com/AbdulRaheemShariff/skills-getting-started1-with-github-copilot/issues/2)
[![GitHub Skills](https://img.shields.io/badge/Explore%20GitHub%20Skills-000000?style=for-the-badge&logo=github&logoColor=white)](https://learn.github.com/skills)

*There's no better way to learn than building things!* 🚀

</div>

---

## Desktop Recorder

This repository also ships a **Desktop Graphics Application Recorder & Player** — a standalone executable that records and replays every mouse and keyboard interaction with any desktop application.

### Where to find the compiled executable

#### Option 1 — Download a pre-built binary from GitHub Releases (recommended)

Every successful build automatically publishes the executables to the [**Releases**](../../releases/tag/latest-build) page as the `latest-build` pre-release. No login required to download.

1. Open the [**Releases**](../../releases/tag/latest-build) page of this repository.
2. Under the `latest-build` release, click the file for your platform:

   | File | Platform |
   |---|---|
   | `desktop_recorder-linux` | Linux (x86-64) |
   | `desktop_recorder-windows.exe` | Windows (x86-64) |
   | `desktop_recorder-macos` | macOS (x86-64) |

3. Run the binary directly — no Python installation required.

> **Tip:** If you prefer, you can also download from the [**Actions**](../../actions/workflows/build-exe.yml) tab. Open the most recent successful run, scroll to the **Artifacts** section, and click the artifact for your OS. Note that downloading workflow artifacts requires you to be signed in to GitHub.

### ⚠️ Windows — "Windows protected your PC" warning

The Windows executable is **signed with a self-signed certificate** (publisher: *Desktop Recorder*), but it has no established SmartScreen reputation because it is an open-source project without a paid EV code-signing certificate.  
Windows Defender SmartScreen will show a blue security dialog the first time you run it.

**Option A — bypass SmartScreen (quickest):**

1. Double-click `desktop_recorder-windows.exe`.
2. In the blue dialog, click **"More info"**.
3. Click **"Run anyway"**.

**Option B — unblock via file Properties:**

1. Right-click `desktop_recorder-windows.exe`.
2. Select **Properties**.
3. At the bottom, check the **"Unblock"** checkbox.
4. Click **OK**, then run the file normally.

**Option C — skip SmartScreen entirely with the Python launcher:**

If Python 3.12+ is already installed you can use `run_windows.bat` instead.
Python scripts are not subject to the SmartScreen reputation check.

```bat
:: Record a session
run_windows.bat record -o my_session.json

:: Replay it
run_windows.bat play -i my_session.json
```

#### Option 2 — Build it yourself locally

```bash
# 1. Install Python 3.12+ and the project dependencies
pip install -r requirements.txt

# 2. Run the build script
python build.py

# 3. The executable is placed in dist/
#    Linux / macOS:  dist/desktop_recorder
#    Windows:        dist/desktop_recorder.exe
```

### Quick-start

```bash
# Record your interactions with any desktop application (press Ctrl+C to stop)
./dist/desktop_recorder record -o my_session.json

# Replay the recording at 1× speed
./dist/desktop_recorder play -i my_session.json

# Replay at 2× speed with event tracing
./dist/desktop_recorder play -i my_session.json --speed 2.0 --verbose

# Inspect the contents of a session file without replaying
./dist/desktop_recorder list -i my_session.json --events
```

---

&copy; 2025 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)

