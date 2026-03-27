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

#### Option 1 — Download a pre-built binary from GitHub Actions (recommended)

Every push to this repository automatically triggers the **"Build Desktop Recorder Executable"** workflow, which compiles the tool for Linux, macOS, and Windows and uploads the result as a downloadable artifact.

To get the binary:

1. Open the [**Actions**](../../actions/workflows/build-exe.yml) tab of this repository.
2. Click the most recent **Build Desktop Recorder Executable** run marked ✅.
3. Scroll to the **Artifacts** section at the bottom of the run page.
4. Download the zip for your operating system:

   | Artifact name | Platform |
   |---|---|
   | `desktop_recorder` | Linux |
   | `desktop_recorder.exe` | Windows |
   | `desktop_recorder-macos` | macOS |

5. Unzip the download and run the binary directly — no Python installation required.

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
&copy; 2025 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)

