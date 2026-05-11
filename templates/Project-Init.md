<%*
/* AutoFlow — Project-Init trigger template
 *
 * Usage:
 *   Cmd+P → "Templater: Create new note from template" → "Project-Init"
 *   (or bind a hotkey via Settings → Hotkeys → Templater)
 *
 * Calls Templates/scripts/projectInit.js which:
 *   - Asks 7 questions
 *   - Creates 02-Projects/<Name>/ with 11 standard files
 *   - Returns a markdown report shown in this scratch file
 *
 * The scratch file can be deleted after reading the report.
 */
const result = await tp.user.projectInit(tp);
tR += result;
%>
