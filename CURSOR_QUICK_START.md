# 🚀 Cursor Quick Start Guide

Welcome to Cursor! Here's how to get the most out of it for your project.

## ✨ Key Cursor Features (vs VS Code)

### 1. **Chat with Your Code** (Cmd/Ctrl + L)
- Ask questions about your codebase
- Get explanations of what code does
- Request changes in natural language
- **Try it**: Press `Cmd+L` (Mac) or `Ctrl+L` (Windows/Linux) and ask "What does consolidate_doctrine.py do?"

### 2. **Composer** (Cmd/Ctrl + I)
- Multi-file editing
- Make changes across multiple files at once
- **Try it**: Press `Cmd+I` and say "Add error handling to all Python scripts"

### 3. **Inline Suggestions** (Tab to accept)
- AI suggests code as you type
- Press `Tab` to accept, `Esc` to dismiss
- Works great for repetitive tasks

### 4. **Codebase-Aware**
- Cursor understands your entire project
- Can reference files, functions, and patterns
- Much smarter than VS Code agents!

## 🎯 Your Workflow in Cursor

### Task: Combine and Proof Doctrine Pages

**Step 1: Combine Pages**
```bash
# Already done! ✅
python3 combine_doctrine_pages.py Doctrines/doctrine-of-divine-essence
```

**Step 2: Consolidate** (in Cursor terminal)
```bash
cd Doctrines/doctrine-of-divine-essence
python3 consolidate_doctrine.py doctrine-of-divine-essence.html
```

**Step 3: Proof** (use Cursor Chat!)
- Press `Cmd+L` (or `Ctrl+L`)
- Say: "Run the proofing tool on doctrine-of-divine-essence_consolidated.html"
- Or manually:
```bash
cd ../..
python3 proof_consolidated_content.py Doctrines/doctrine-of-divine-essence/doctrine-of-divine-essence_consolidated.html
```

**Step 4: Review**
- Open the review report in Cursor
- Use `Cmd+L` to ask: "What issues were found in the consolidated file?"
- Fix issues directly in Cursor

## 💡 Pro Tips

### 1. **Use Chat for Everything**
Instead of searching docs, just ask Cursor:
- "How do I run the consolidation script?"
- "What's the difference between consolidated and standalone files?"
- "Show me all files that reference 'divine essence'"

### 2. **Multi-File Edits**
Need to update URLs in multiple files?
- Press `Cmd+I` (Composer)
- Say: "Update all WordPress URLs to use intelligencereport.info"
- Cursor will find and update all instances

### 3. **Quick File Navigation**
- `Cmd+P` (Mac) or `Ctrl+P` (Windows): Quick file search
- Type part of filename to jump to it
- Much faster than clicking through folders

### 4. **Terminal Integration**
- Terminal is built-in (bottom panel)
- Can run commands while chatting with Cursor
- Cursor can suggest commands based on your task

### 5. **Ask for Explanations**
Don't understand a script? Just ask:
- Click on `consolidate_doctrine.py`
- Press `Cmd+L`
- Ask: "Explain how this script works"

## 🎨 Cursor vs VS Code Agents

| Feature | VS Code Agents | Cursor |
|---------|---------------|--------|
| Codebase awareness | Limited | Full project understanding |
| Multi-file edits | Difficult | Easy (Composer) |
| Natural language | Basic | Excellent |
| Context retention | Poor | Great |
| File navigation | Manual | AI-assisted |

## 🔥 Your Current Project Setup

### Files You'll Use Most:

1. **`combine_doctrine_pages.py`** - Combines TOC + pages 1-33
2. **`consolidate_doctrine.py`** - Merges HTML fragments
3. **`proof_consolidated_content.py`** - Reviews content
4. **`generate_standalone_doctrine_page.py`** - Creates WordPress pages

### Quick Commands Reference:

```bash
# Combine pages
python3 combine_doctrine_pages.py Doctrines/doctrine-of-divine-essence

# Consolidate
cd Doctrines/doctrine-of-divine-essence
python3 consolidate_doctrine.py doctrine-of-divine-essence.html

# Proof
cd ../..
python3 proof_consolidated_content.py Doctrines/doctrine-of-divine-essence/doctrine-of-divine-essence_consolidated.html

# Generate WordPress page
python3 generate_standalone_doctrine_page.py "Doctrine Name" consolidated_file.html
```

## 🎓 Learning Cursor

### Start Here:
1. **Open any Python file**
2. **Press `Cmd+L`** (or `Ctrl+L`)
3. **Ask**: "What does this file do?"
4. **Try**: "Add comments explaining each function"

### Next Level:
1. **Select multiple files** (Cmd+Click)
2. **Press `Cmd+I`** (Composer)
3. **Say**: "Add error handling to all these scripts"

### Pro Move:
1. **Press `Cmd+L`**
2. **Ask**: "Show me all places where we reference WordPress URLs"
3. **Then**: "Update them all to use the new domain"

## 🐛 Troubleshooting

**Cursor not responding?**
- Check if you're in a chat (`Cmd+L`)
- Try `Esc` to exit chat mode
- Restart Cursor if needed

**Can't find a file?**
- Use `Cmd+P` to search
- Or ask Cursor: "Where is consolidate_doctrine.py?"

**Script not working?**
- Ask Cursor: "Why isn't this script working?"
- Paste the error message
- Cursor will help debug!

## 🎉 You're Ready!

Cursor is now your coding partner. Just talk to it naturally:
- "Help me combine these files"
- "What errors are in this code?"
- "Show me how to use this script"
- "Fix this bug"

**Remember**: Cursor understands your entire project, so be specific about what you want!

---

**Next Steps for Your Project:**
1. ✅ Combined TOC + pages 1-33
2. ⏳ Consolidate the combined file
3. ⏳ Proof the consolidated content
4. ⏳ Review and fix issues
5. ⏳ Generate WordPress page when ready

**Need help?** Just press `Cmd+L` and ask! 🚀
