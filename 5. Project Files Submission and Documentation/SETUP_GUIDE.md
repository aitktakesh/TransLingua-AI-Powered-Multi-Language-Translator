# TransLingua - Quick Setup Guide

## Prerequisites Check
✅ Python 3.8+ installed
✅ pip package manager
✅ Internet connection
✅ Google Gemini API key

## One-Time Setup (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

**Expected output**: Successfully installed streamlit, google-generativeai, python-dotenv

---

### Step 2: Configure API Key

1. Get your free API key from: https://makersuite.google.com/app/apikey

2. Create a `.env` file in the project root:
```bash
# Copy the template
copy .env.example .env

# Or on macOS/Linux:
cp .env.example .env
```

3. Edit `.env` and add your API key:
```
GOOGLE_API_KEY=AIzaSy...your_actual_key_here
```

**⚠️ IMPORTANT**: 
- Never share your API key
- Never commit `.env` to version control
- Keep it secure

---

### Step 3: Run the Application
```bash
streamlit run app.py
```

**What happens**:
1. Streamlit server starts on port 8501
2. Browser automatically opens to http://localhost:8501
3. Application is ready to use!

---

## First Translation Test

1. **Select Source Language**: English
2. **Select Target Language**: Spanish
3. **Enter Text**: Hello, how are you?
4. **Click**: 🔄 Translate
5. **Result**: Hola, ¿cómo estás?

---

## Common Issues & Solutions

### Issue: "API Key not found"
**Solution**: 
- Ensure `.env` file exists in the project root
- Verify `GOOGLE_API_KEY` is spelled correctly
- Check for extra spaces in the `.env` file

### Issue: "Module not found"
**Solution**:
```bash
pip install -r requirements.txt --upgrade
```

### Issue: "Address already in use"
**Solution**:
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

### Issue: Translation fails
**Solution**:
- Check internet connection
- Verify API key is valid
- Check API quota limits

---

## Quick Commands Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py

# Run on custom port
streamlit run app.py --server.port 8502

# Run in browser
streamlit run app.py --server.headless false

# Check Streamlit version
streamlit --version

# Check Python version
python --version
```

---

## Project Structure
```
TransLingua/
│
├── app.py                      # Main application (run this)
├── requirements.txt            # Dependencies
├── .env                        # Your API key (create this)
├── .env.example               # Template
├── .gitignore                 # Git ignore rules
├── README.md                  # Full documentation
├── CODE_EXPLANATION.md        # Code walkthrough
├── FUTURE_ENHANCEMENTS.md     # Enhancement ideas
└── SETUP_GUIDE.md            # This file
```

---

## Stopping the Application

**In terminal**: Press `Ctrl + C`

The server will gracefully shut down.

---

## Next Steps

1. ✅ Complete setup
2. ✅ Test basic translation
3. 📖 Read CODE_EXPLANATION.md to understand the code
4. 🚀 Explore FUTURE_ENHANCEMENTS.md for ideas
5. 🌐 Deploy to Streamlit Cloud (optional)

---

## Deployment to Streamlit Cloud (Optional)

### Why Deploy?
- Share with others
- Access from anywhere
- Free hosting

### Steps:
1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect GitHub repository
4. Add `GOOGLE_API_KEY` to Secrets
5. Deploy!

**Secrets format** (in Streamlit Cloud):
```toml
GOOGLE_API_KEY = "your_api_key_here"
```

---

## Support

- 📖 Read README.md for detailed documentation
- 🐛 Check Common Issues section above
- 💬 Review code comments in app.py

---

**You're all set! Happy translating! 🌐**
