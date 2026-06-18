# import streamlit as st
# import logging
# import time
# from translation import TranslateGemmaTranslator
# from main_1 import main
# from evaluation import TranslationEvaluator

# # -----------------------
# # Logging
# # -----------------------
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger("TranslateGemmaUI")

# st.set_page_config(
#     page_title="Patent Summary Translator",
#     layout="wide"
# )

# st.title("🔄 Patent Summary Translator with Evaluation")
# st.markdown("Translate patent summaries using TranslateGemma and evaluate quality with LLM metrics")

# # -----------------------
# # Cache Models (Critical)
# # -----------------------
# @st.cache_resource
# def load_translator():
#     """Load translation model"""
#     logger.info("Loading translation model...")
#     return TranslateGemmaTranslator()


# @st.cache_resource
# def load_evaluator():
#     """Load evaluation model"""
#     logger.info("Loading evaluation model...")
#     return TranslationEvaluator(verbose=False)


# try:
#     with st.spinner("⏳ Loading models (may take 2-3 minutes on first run)..."):
#         translator = load_translator()
#         evaluator = load_evaluator()
#     st.success("✅ Models loaded successfully!")
# except Exception as e:
#     st.error(f"❌ Failed to load models: {str(e)}")
#     st.stop()

# # -----------------------
# # Input Section
# # -----------------------
# st.subheader("📝 Input")
# col_input = st.columns([1])[0]

# with col_input:
#     pnkc = st.text_input("Enter PNKC", placeholder="e.g. US1234567A")
#     translate_btn = st.button("🚀 Translate & Evaluate", use_container_width=True)

# # -----------------------
# # Translation Execution
# # -----------------------
# if translate_btn:
#     if not pnkc.strip():
#         st.error("❌ PNKC cannot be empty.")
#         st.stop()
    
#     # Translate
#     with st.spinner("⏳ Translating..."):
#         result = main(pnkc.strip(), translator)
    
#     if not result:
#         st.error("❌ Document not found or summary missing.")
#         st.stop()
    
#     # Now show 3-column layout
#     st.divider()
#     st.subheader("📊 Results")
    
#     col1, col2, col3 = st.columns([1, 1, 1], gap="medium")
    
#     # =====================
#     # COLUMN 1: Source Text
#     # =====================
#     with col1:
#         st.markdown("### 📄 Source Summary")
#         st.text_area(
#             label="Source Text",
#             value=result["source_text"],
#             height=400,
#             disabled=True,
#             key="source_area"
#         )
        
#         # Metadata
#         st.markdown("---")
#         st.markdown("**Metadata:**")
#         st.write(f"- **PNKC:** {result['pnkc']}")
#         st.write(f"- **Inference Time:** {result['latency']:.2f}s")
    
#     # =====================
#     # COLUMN 2: Translation
#     # =====================
#     with col2:
#         st.markdown("### 🌐 Translated Summary")
#         st.text_area(
#             label="Translated Text",
#             value=result["translated_text"],
#             height=400,
#             disabled=True,
#             key="translated_area"
#         )
    
#     # =====================
#     # COLUMN 3: Evaluation
#     # =====================
#     with col3:
#         st.markdown("### 📈 Quality Evaluation")
        
#         with st.spinner("⏳ Evaluating translation quality..."):
#             try:
#                 eval_result = evaluator.evaluate_translation(
#                     source_text=result["source_text"],
#                     translated_text=result["translated_text"]
#                 )
                
#                 # Overall Score
#                 st.metric(
#                     label="Overall Score",
#                     value=f"{eval_result['overall_score']:.3f}",
#                     delta=None,
#                     help="Average of all metrics (0-1 scale)"
#                 )
                
#                 # Pass/Fail Status
#                 col_pass, col_fail = st.columns(2)
#                 with col_pass:
#                     st.metric(
#                         label="✅ Passed",
#                         value=eval_result['passed']
#                     )
#                 with col_fail:
#                     st.metric(
#                         label="❌ Failed",
#                         value=eval_result['failed']
#                     )
                
#                 st.markdown("---")
                
#                 # Individual Metrics
#                 st.markdown("**Metric Scores:**")
#                 for metric in eval_result['metrics']:
#                     # Metric header with pass/fail indicator
#                     status_icon = "✅" if metric['passed'] else "❌"
#                     st.markdown(
#                         f"**{status_icon} {metric['name']}**"
#                     )
                    
#                     # Score as progress bar
#                     st.progress(
#                         value=metric['score'],
#                         text=f"{metric['score']:.3f}"
#                     )
                    
#                     # Reason
#                     st.caption(f"📝 {metric['reason']}")
#                     st.markdown("")
            
#             except Exception as e:
#                 st.error(f"❌ Evaluation failed: {str(e)}")
#                 logger.exception("Evaluation error")
    
#     # =====================
#     # Summary Table
#     # =====================
#     st.divider()
#     st.subheader("📋 Summary Table")
    
#     summary_data = {
#         "Metric": [m['name'] for m in eval_result['metrics']],
#         "Score": [f"{m['score']:.3f}" for m in eval_result['metrics']],
#         "Status": ["✅ Pass" if m['passed'] else "❌ Fail" for m in eval_result['metrics']],
#         "Reason": [m['reason'] for m in eval_result['metrics']]
#     }
    
#     st.dataframe(
#         summary_data,
#         use_container_width=True,
#         hide_index=True
#     )


# import streamlit as st
# import logging
# import time
# from translation import TranslateGemmaTranslator
# from main_1 import main
# from evaluation import TranslationEvaluator
# import os

# # Configure Streamlit for IPv6
# os.environ['STREAMLIT_SERVER_ADDRESS'] = '::'
# os.environ['STREAMLIT_SERVER_PORT'] = '8501'

# # -----------------------
# # Logging
# # -----------------------
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger("TranslateGemmaUI")

# st.set_page_config(
#     page_title="Patent Summary Translator",
#     layout="wide"
# )

# st.title("🔄 Patent Summary Translator with Evaluation")
# st.markdown("Translate patent summaries using TranslateGemma and evaluate quality with LLM metrics")

# # -----------------------
# # Get API Key
# # -----------------------

# api_key = os.getenv("OPENAI_API_KEY","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")
# if not api_key:
#     st.error("❌ OPENAI_API_KEY environment variable not set")
#     st.stop()

# # -----------------------
# # Cache Models (Critical)
# # -----------------------
# @st.cache_resource
# def load_translator():
#     """Load translation model"""
#     logger.info("Loading translation model...")
#     return TranslateGemmaTranslator()


# @st.cache_resource
# def load_evaluator():
#     """Load evaluation model with OpenAI API key"""
#     logger.info("Loading evaluation model...")
#     return TranslationEvaluator(api_key=api_key)


# try:
#     with st.spinner("⏳ Loading models (may take 2-3 minutes on first run)..."):
#         translator = load_translator()
#         evaluator = load_evaluator()
#     st.success("✅ Models loaded successfully!")
# except Exception as e:
#     st.error(f"❌ Failed to load models: {str(e)}")
#     logger.exception("Model loading error")
#     st.stop()

# # -----------------------
# # Input Section
# # -----------------------
# st.subheader("📝 Input")
# col_input = st.columns([1])[0]

# with col_input:
#     pnkc = st.text_input("Enter PNKC", placeholder="e.g. US1234567A")
#     translate_btn = st.button("🚀 Translate & Evaluate", use_container_width=True)

# # -----------------------
# # Translation Execution
# # -----------------------
# if translate_btn:
#     if not pnkc.strip():
#         st.error("❌ PNKC cannot be empty.")
#         st.stop()
    
#     # Translate
#     with st.spinner("⏳ Translating..."):
#         result = main(pnkc.strip(), translator)
    
#     if not result:
#         st.error("❌ Document not found or summary missing.")
#         st.stop()
    
#     # Now show 3-column layout
#     st.divider()
#     st.subheader("📊 Results")
    
#     col1, col2, col3 = st.columns([1, 1, 1], gap="medium")
    
#     # =====================
#     # COLUMN 1: Source Text
#     # =====================
#     with col1:
#         st.markdown("### 📄 Source Summary")
#         st.text_area(
#             label="Source Text",
#             value=result["source_text"],
#             height=400,
#             disabled=True,
#             key="source_area"
#         )
        
#         # Metadata
#         st.markdown("---")
#         st.markdown("**Metadata:**")
#         st.write(f"- **PNKC:** {result['pnkc']}")
#         st.write(f"- **Inference Time:** {result['latency']:.2f}s")
    
#     # =====================
#     # COLUMN 2: Translation
#     # =====================
#     with col2:
#         st.markdown("### 🌐 Translated Summary")
#         st.text_area(
#             label="Translated Text",
#             value=result["translated_text"],
#             height=400,
#             disabled=True,
#             key="translated_area"
#         )
    
#     # =====================
#     # COLUMN 3: Evaluation
#     # =====================
#     with col3:
#         st.markdown("### 📈 Quality Evaluation")
        
#         with st.spinner("⏳ Evaluating translation quality..."):
#             try:
#                 eval_result = evaluator.evaluate_translation(
#                     source_text=result["source_text"],
#                     translated_text=result["translated_text"]
#                 )
                
#                 # Overall Score
#                 st.metric(
#                     label="Overall Score",
#                     value=f"{eval_result['overall_score']:.3f}",
#                     delta=None,
#                     help="Average of all metrics (0-1 scale)"
#                 )
                
#                 # Pass/Fail Status
#                 col_pass, col_fail = st.columns(2)
#                 with col_pass:
#                     st.metric(
#                         label="✅ Passed",
#                         value=eval_result['passed_metrics']
#                     )
#                 with col_fail:
#                     st.metric(
#                         label="❌ Failed",
#                         value=eval_result['failed_metrics']
#                     )
                
#                 st.markdown("---")
                
#                 # Individual Metrics
#                 st.markdown("**Metric Scores:**")
#                 for metric in eval_result['metrics']:
#                     # Metric header with pass/fail indicator
#                     status_icon = "✅" if metric['passed'] else "❌"
#                     st.markdown(
#                         f"**{status_icon} {metric['metric']}**"
#                     )
                    
#                     # Score as progress bar
#                     st.progress(
#                         value=metric['score'],
#                         text=f"{metric['score']:.3f}"
#                     )
                    
#                     # Reason
#                     if metric.get('reason'):
#                         st.caption(f"📝 {metric['reason']}")
#                     st.markdown("")
            
#             except Exception as e:
#                 st.error(f"❌ Evaluation failed: {str(e)}")
#                 logger.exception("Evaluation error")
    
#     # =====================
#     # Summary Table
#     # =====================
#     st.divider()
#     st.subheader("📋 Summary Table")
    
#     try:
#         summary_data = {
#             "Metric": [m['metric'] for m in eval_result['metrics']],
#             "Score": [f"{m['score']:.3f}" for m in eval_result['metrics']],
#             "Status": ["✅ Pass" if m['passed'] else "❌ Fail" for m in eval_result['metrics']],
#             "Reason": [m.get('reason', 'N/A') for m in eval_result['metrics']]
#         }
        
#         st.dataframe(
#             summary_data,
#             use_container_width=True,
#             hide_index=True
#         )
#     except Exception as e:
#         st.error(f"Error displaying table: {str(e)}")
#         logger.exception("Table display error")


####################### with alma ###########################


import streamlit as st
import logging
import time
from translation import TranslateGemmaTranslator, XALMATranslator
from main_1 import main
from evaluation import TranslationEvaluator
import os

# Configure Streamlit for IPv6
os.environ['STREAMLIT_SERVER_ADDRESS'] = '::'
os.environ['STREAMLIT_SERVER_PORT'] = '8501'

# -----------------------
# Logging
# -----------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PatentTranslatorUI")

st.set_page_config(
    page_title="Patent Summary Translator",
    layout="wide"
)

st.title("🔄 Patent Summary Translator with Evaluation")
st.markdown("Translate patent summaries using multiple AI models and evaluate quality with LLM metrics")

# -----------------------
# Get API Key
# -----------------------

api_key = os.getenv("OPENAI_API_KEY","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")
if not api_key:
    st.error("❌ OPENAI_API_KEY environment variable not set")
    st.stop()

# -----------------------
# Cache Models (Critical)
# -----------------------
@st.cache_resource
def load_translate_gemma_translator():
    """Load TranslateGemma translation model"""
    logger.info("Loading TranslateGemma translation model...")
    return TranslateGemmaTranslator()


@st.cache_resource
def load_xalma_translator(group_id: str = "6"):
    """Load X-ALMA translation model"""
    logger.info(f"Loading X-ALMA translation model (Group {group_id})...")
    return XALMATranslator(group_id=group_id)


@st.cache_resource
def load_evaluator():
    """Load evaluation model with OpenAI API key"""
    logger.info("Loading evaluation model...")
    return TranslationEvaluator(api_key=api_key)


# -----------------------
# Load Models
# -----------------------
models_to_load = {}
try:
    with st.spinner("⏳ Loading models (may take 2-3 minutes on first run)..."):
        models_to_load['gemma'] = load_translate_gemma_translator()
        models_to_load['xalma'] = load_xalma_translator(group_id="6")
        evaluator = load_evaluator()
    st.success("✅ All models loaded successfully!")
except Exception as e:
    st.error(f"❌ Failed to load models: {str(e)}")
    logger.exception("Model loading error")
    st.stop()

# -----------------------
# Sidebar Configuration
# -----------------------
st.sidebar.title("⚙️ Configuration")

# Model Selection
st.sidebar.markdown("### 🤖 Translation Model")
selected_model = st.sidebar.radio(
    "Choose translation model:",
    options=["TranslateGemma", "X-ALMA"],
    help="TranslateGemma: Fast, multimodal-capable\nX-ALMA: Latest generation, 50 languages"
)

# Model Information
if selected_model == "TranslateGemma":
    with st.sidebar.expander("ℹ️ TranslateGemma Info"):
        st.markdown("""
        **TranslateGemma Translator**
        
        - **Type:** Multimodal translation
        - **Architecture:** Image-text-to-text
        - **Languages:** Multiple (configured)
        - **Advantage:** Fast inference, multimodal support
        - **Use Case:** General-purpose translation
        """)
else:
    with st.sidebar.expander("ℹ️ X-ALMA Info"):
        st.markdown("""
        **X-ALMA Translator**
        
        - **Type:** LLM-based translation
        - **Architecture:** LLaMA-2 with language modules
        - **Languages:** 50 languages (8 groups)
        - **Current Group:** 6 (East Asian - includes Japanese)
        - **Advantage:** State-of-the-art quality, multilingual
        - **Use Case:** High-quality, multilingual translation
        - **Paper:** ICLR 2025
        """)

# X-ALMA Group Selection (if X-ALMA is selected)
if selected_model == "X-ALMA":
    st.sidebar.markdown("### 🌍 X-ALMA Language Group")
    group_options = {
        "1 - European (DA, NL, DE, IS, NO, SV, AF)": "1",
        "2 - Romance (CA, RO, GL, IT, PT, ES)": "2",
        "3 - Slavic (BG, MK, SR, UK, RU)": "3",
        "4 - Asian+French (ID, MS, TH, VI, MG, FR)": "4",
        "5 - European (HU, EL, CS, PL, LT, LV)": "5",
        "6 - East Asian (KA, ZH, JA, KO, FI, ET)": "6",
        "7 - South Asian (GU, HI, MR, NE, UR)": "7",
        "8 - Middle East/Central Asian (AZ, KK, KY, TR, UZ, AR, HE, FA)": "8",
    }
    
    selected_group_label = st.sidebar.selectbox(
        "Select language group:",
        options=group_options.keys(),
        index=5,  # Default to Group 6
        help="Select the group containing your target language"
    )
    selected_group = group_options[selected_group_label]
    
    # Reload X-ALMA with selected group
    if selected_group != "6":
        try:
            with st.spinner(f"⏳ Loading X-ALMA Group {selected_group}..."):
                models_to_load['xalma'] = load_xalma_translator(group_id=selected_group)
            st.sidebar.success(f"✅ Loaded Group {selected_group}")
        except Exception as e:
            st.sidebar.error(f"❌ Failed to load group: {str(e)}")

# Language Pair Settings
st.sidebar.markdown("### 🌐 Language Settings")
col_source, col_target = st.sidebar.columns(2)

with col_source:
    source_lang = st.text_input(
        "Source Language",
        value="English",
        help="Source language for translation"
    )

with col_target:
    target_lang = st.text_input(
        "Target Language",
        value="Japanese",
        help="Target language for translation"
    )

# -----------------------
# Input Section
# -----------------------
st.subheader("📝 Input")

col_input = st.columns([1])[0]

with col_input:
    pnkc = st.text_input(
        "Enter PNKC (Patent Number)",
        placeholder="e.g. US1234567A",
        help="Patent number to fetch and translate"
    )
    
    col_button_1, col_button_2 = st.columns(2)
    
    with col_button_1:
        translate_btn = st.button(
            "🚀 Translate & Evaluate",
            use_container_width=True,
            help=f"Translate using {selected_model}"
        )
    
    with col_button_2:
        compare_btn = st.button(
            "⚖️ Compare Models",
            use_container_width=True,
            help="Compare translations from both models"
        )

# -----------------------
# Single Model Translation
# -----------------------
if translate_btn:
    if not pnkc.strip():
        st.error("❌ PNKC cannot be empty.")
        st.stop()
    
    # Select translator based on choice
    if selected_model == "TranslateGemma":
        translator = models_to_load['gemma']
        model_display_name = "TranslateGemma"
    else:
        translator = models_to_load['xalma']
        model_display_name = f"X-ALMA (Group {selected_group})"
    
    # Translate
    with st.spinner(f"⏳ Translating with {model_display_name}..."):
        result = main(pnkc.strip(), translator)
    
    if not result:
        st.error("❌ Document not found or summary missing.")
        st.stop()
    
    # Now show 3-column layout
    st.divider()
    st.subheader(f"📊 Results - {model_display_name}")
    
    col1, col2, col3 = st.columns([1, 1, 1], gap="medium")
    
    # =====================
    # COLUMN 1: Source Text
    # =====================
    with col1:
        st.markdown("### 📄 Source Summary")
        st.text_area(
            label="Source Text",
            value=result["source_text"],
            height=400,
            disabled=True,
            key="source_area"
        )
        
        # Metadata
        st.markdown("---")
        st.markdown("**Metadata:**")
        st.write(f"- **PNKC:** {result['pnkc']}")
        st.write(f"- **Model:** {model_display_name}")
        st.write(f"- **Inference Time:** {result['latency']:.2f}s")
        st.write(f"- **Characters:** {len(result['source_text'])}")
    
    # =====================
    # COLUMN 2: Translation
    # =====================
    with col2:
        st.markdown("### 🌐 Translated Summary")
        st.text_area(
            label="Translated Text",
            value=result["translated_text"],
            height=400,
            disabled=True,
            key="translated_area"
        )
        
        # Translation Metadata
        st.markdown("---")
        st.markdown("**Translation Info:**")
        st.write(f"- **Source Language:** {source_lang}")
        st.write(f"- **Target Language:** {target_lang}")
        st.write(f"- **Characters:** {len(result['translated_text'])}")
    
    # =====================
    # COLUMN 3: Evaluation
    # =====================
    with col3:
        st.markdown("### 📈 Quality Evaluation")
        
        with st.spinner("⏳ Evaluating translation quality..."):
            try:
                eval_result = evaluator.evaluate_translation(
                    source_text=result["source_text"],
                    translated_text=result["translated_text"]
                )
                
                # Overall Score
                st.metric(
                    label="Overall Score",
                    value=f"{eval_result['overall_score']:.3f}",
                    delta=None,
                    help="Average of all metrics (0-1 scale)"
                )
                
                # Pass/Fail Status
                col_pass, col_fail = st.columns(2)
                with col_pass:
                    st.metric(
                        label="✅ Passed",
                        value=eval_result['passed_metrics']
                    )
                with col_fail:
                    st.metric(
                        label="❌ Failed",
                        value=eval_result['failed_metrics']
                    )
                
                st.markdown("---")
                
                # Individual Metrics
                st.markdown("**Metric Scores:**")
                for metric in eval_result['metrics']:
                    # Metric header with pass/fail indicator
                    status_icon = "✅" if metric['passed'] else "❌"
                    st.markdown(
                        f"**{status_icon} {metric['metric']}**"
                    )
                    
                    # Score as progress bar
                    st.progress(
                        value=metric['score'],
                        text=f"{metric['score']:.3f}"
                    )
                    
                    # Reason
                    if metric.get('reason'):
                        st.caption(f"📝 {metric['reason']}")
                    st.markdown("")
            
            except Exception as e:
                st.error(f"❌ Evaluation failed: {str(e)}")
                logger.exception("Evaluation error")
    
    # =====================
    # Summary Table
    # =====================
    st.divider()
    st.subheader("📋 Evaluation Summary Table")
    
    try:
        summary_data = {
            "Metric": [m['metric'] for m in eval_result['metrics']],
            "Score": [f"{m['score']:.3f}" for m in eval_result['metrics']],
            "Status": ["✅ Pass" if m['passed'] else "❌ Fail" for m in eval_result['metrics']],
            "Reason": [m.get('reason', 'N/A') for m in eval_result['metrics']]
        }
        
        st.dataframe(
            summary_data,
            use_container_width=True,
            hide_index=True
        )
    except Exception as e:
        st.error(f"Error displaying table: {str(e)}")
        logger.exception("Table display error")


# -----------------------
# Model Comparison
# -----------------------
if compare_btn:
    if not pnkc.strip():
        st.error("❌ PNKC cannot be empty.")
        st.stop()
    
    st.divider()
    st.subheader("⚖️ Model Comparison")
    st.info("This will translate using both models and compare results")
    
    # Create two columns for parallel translation
    col_gemma, col_xalma = st.columns(2)
    
    # =====================================
    # GEMMA TRANSLATION
    # =====================================
    with col_gemma:
        st.markdown("### 🤖 TranslateGemma")
        
        with st.spinner("⏳ Translating with TranslateGemma..."):
            try:
                gemma_translator = models_to_load['gemma']
                gemma_result = main(pnkc.strip(), gemma_translator)
                
                if gemma_result:
                    st.markdown("#### Source")
                    st.text_area(
                        label="Gemma Source",
                        value=gemma_result["source_text"][:500] + "...",
                        height=150,
                        disabled=True,
                        key="gemma_source"
                    )
                    
                    st.markdown("#### Translation")
                    st.text_area(
                        label="Gemma Translation",
                        value=gemma_result["translated_text"],
                        height=250,
                        disabled=True,
                        key="gemma_translated"
                    )
                    
                    st.markdown("---")
                    st.markdown("**Metadata:**")
                    st.write(f"- **Inference Time:** {gemma_result['latency']:.2f}s")
                    st.write(f"- **Characters:** {len(gemma_result['translated_text'])}")
                    
                    # Evaluate Gemma
                    with st.spinner("⏳ Evaluating Gemma..."):
                        gemma_eval = evaluator.evaluate_translation(
                            source_text=gemma_result["source_text"],
                            translated_text=gemma_result["translated_text"]
                        )
                    
                    st.markdown("#### Quality Score")
                    st.metric(
                        "Overall Score",
                        f"{gemma_eval['overall_score']:.3f}"
                    )
                else:
                    st.error("❌ Failed to translate with TranslateGemma")
            
            except Exception as e:
                st.error(f"❌ TranslateGemma error: {str(e)}")
                logger.exception("TranslateGemma error")
    
    # =====================================
    # X-ALMA TRANSLATION
    # =====================================
    with col_xalma:
        st.markdown("### 🧠 X-ALMA")
        
        with st.spinner(f"⏳ Translating with X-ALMA (Group {selected_group})..."):
            try:
                xalma_translator = models_to_load['xalma']
                xalma_result = main(pnkc.strip(), xalma_translator)
                
                if xalma_result:
                    st.markdown("#### Source")
                    st.text_area(
                        label="X-ALMA Source",
                        value=xalma_result["source_text"][:500] + "...",
                        height=150,
                        disabled=True,
                        key="xalma_source"
                    )
                    
                    st.markdown("#### Translation")
                    st.text_area(
                        label="X-ALMA Translation",
                        value=xalma_result["translated_text"],
                        height=250,
                        disabled=True,
                        key="xalma_translated"
                    )
                    
                    st.markdown("---")
                    st.markdown("**Metadata:**")
                    st.write(f"- **Inference Time:** {xalma_result['latency']:.2f}s")
                    st.write(f"- **Characters:** {len(xalma_result['translated_text'])}")
                    
                    # Evaluate X-ALMA
                    with st.spinner("⏳ Evaluating X-ALMA..."):
                        xalma_eval = evaluator.evaluate_translation(
                            source_text=xalma_result["source_text"],
                            translated_text=xalma_result["translated_text"]
                        )
                    
                    st.markdown("#### Quality Score")
                    st.metric(
                        "Overall Score",
                        f"{xalma_eval['overall_score']:.3f}"
                    )
                else:
                    st.error("❌ Failed to translate with X-ALMA")
            
            except Exception as e:
                st.error(f"❌ X-ALMA error: {str(e)}")
                logger.exception("X-ALMA error")
    
    # =====================================
    # COMPARISON SUMMARY
    # =====================================
    st.divider()
    st.subheader("📊 Comparison Summary")
    
    try:
        if 'gemma_eval' in locals() and 'xalma_eval' in locals():
            comparison_data = {
                "Metric": [m['metric'] for m in gemma_eval['metrics']],
                "TranslateGemma": [f"{m['score']:.3f}" for m in gemma_eval['metrics']],
                "X-ALMA": [f"{m['score']:.3f}" for m in xalma_eval['metrics']],
                "Difference": [
                    f"{(xalma_eval['metrics'][i]['score'] - gemma_eval['metrics'][i]['score']):.3f}"
                    for i in range(len(gemma_eval['metrics']))
                ]
            }
            
            st.dataframe(
                comparison_data,
                use_container_width=True,
                hide_index=True
            )
            
            # Winner announcement
            gemma_score = gemma_eval['overall_score']
            xalma_score = xalma_eval['overall_score']
            
            col_winner_1, col_winner_2, col_winner_3 = st.columns(3)
            
            with col_winner_1:
                st.metric("TranslateGemma Score", f"{gemma_score:.3f}")
            
            with col_winner_2:
                if abs(xalma_score - gemma_score) < 0.01:
                    st.info("🤝 **TIED** - Both models perform equally")
                elif xalma_score > gemma_score:
                    diff = xalma_score - gemma_score
                    st.success(f"🏆 **X-ALMA WINS** by {diff:.3f}")
                else:
                    diff = gemma_score - xalma_score
                    st.success(f"🏆 **TranslateGemma WINS** by {diff:.3f}")
            
            with col_winner_3:
                st.metric("X-ALMA Score", f"{xalma_score:.3f}")
    
    except Exception as e:
        st.error(f"Error in comparison: {str(e)}")
        logger.exception("Comparison error")

# -----------------------
# Footer
# -----------------------
st.divider()
st.markdown("""
<div style='text-align: center'>
    <p style='color: #888'>
        Patent Summary Translator v2.0 | 
        Models: TranslateGemma & X-ALMA-13B | 
        Evaluator: OpenAI GPT-4
    </p>
</div>
""", unsafe_allow_html=True)