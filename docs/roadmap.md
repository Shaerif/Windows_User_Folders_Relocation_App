# Project Roadmap

## Milestones

### Phase 1: Initial Implementation
- **Core Functionality:** Implement the core functionality for relocating user folders.
- **Logging and Progress Tracking:** Add logging and progress tracking.
- **Safety Measures:** Ensure safety measures like registry backup and file verification.

### Phase 2: GUI Enhancements
- **Add GUI Options:** Add options in the GUI to skip checksum validation, delete files after relocation, and use the new location as the default for Windows.
- **Improve Error Handling:** Enhance error handling to provide more informative messages and recovery options.

### Phase 3: Performance Optimization
- **Optimize Performance:** Optimize the script for faster file operations and lower resource usage.
- **Add More Folder Types:** Expand the list of supported folders that can be relocated.

### Phase 4: User Feedback and Documentation
- **User Feedback:** Implement a feedback mechanism to gather user input and improve the tool.
- **Documentation:** Create detailed documentation for developers and users.

### Phase 5: CLI & GUI Dual Options
- **Allow Both CLI and GUI Use**: Make it possible to run the tool in either CLI or GUI mode at the user's discretion.
- **Documentation Update**: Reflect the new dual-run capability throughout all relevant documentation.

### Phase 6: Future Enhancements
- **Additional Features:** Explore additional features based on user feedback and project requirements.
- **Community Contributions:** Encourage community contributions and collaboration.

## Detailed Tasks

1. **Ensure User Files are Moved and Checksummed Before Removal**
   - Update the script to verify file integrity before removing files from the original location.

2. **Add GUI Options**
   - Add options in the GUI to skip checksum validation, delete files after relocation, and use the new location as the default for Windows.

3. **Update Readme**
   - Add detailed information about relocating user-specific folders and using new locations as default.

4. **Compile to Executable**
   - Ensure the script can be compiled to an executable format using `PyInstaller`.

5. **Improve Error Handling**
   - Enhance error handling to provide more informative messages and recovery options.

6. **Add More Folder Types**
   - Expand the list of supported folders that can be relocated.

7. **Optimize Performance**
   - Optimize the script for faster file operations and lower resource usage.

8. **User Feedback**
   - Implement a feedback mechanism to gather user input and improve the tool.

9. **Documentation**
   - Create detailed documentation for developers and users.

10. **Add Option to Clear Log on Exit**
    - Add an option in the GUI to clear the log on exit.

11. **Create or Update Documentation**
    - In the `docs` folder, create or update `tasks.md` outlining the project's tasks, a `roadmap.md` detailing the project's milestones, and a file explaining the project's architecture and file usage. Specifically, analyze all files in the project and provide a description of each file's purpose and how it contributes to the overall project.

12. **Generate Detailed Report**
    - Update the script to generate a detailed report of the relocation process in both the GUI and CLI, including files moved, size of files, and any errors encountered.
