@echo off
REM Setze das Zielverzeichnis
SET "TARGET_DIR=C:\Users\elex\Documents\GitHub\Kimba_AI\models"

REM LLMs
huggingface-cli download TheBloke/Llama-3.1-8B-Instruct-GGUF --include "llama3.1-8b-instruct.Q4_K_M.gguf" --local-dir "%TARGET_DIR%\llm\core"
huggingface-cli download TheBloke/MythoMax-L2-13B-GGUF --include "mythomax-l2-13b.Q4_K_M.gguf" --local-dir "%TARGET_DIR%\llm\creative"
huggingface-cli download TheBloke/dolphin-2.9-mixtral-8x7b-GGUF --include "dolphin-2.9-mixtral-8x7b.Q4_K_M.gguf" --local-dir "%TARGET_DIR%\llm\empathy"
huggingface-cli download deepseek-ai/deepseek-coder-6.7b-base-GGUF --include "deepseek-coder.Q4_K_M.gguf" --local-dir "%TARGET_DIR%\llm\code"
huggingface-cli download TheBloke/Command-R-Plus-GGUF --include "command-r-plus.Q4_K_M.gguf" --local-dir "%TARGET_DIR%\llm\multimodal"
huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.2-GGUF --include "mistral-7b-instruct-v0.2.Q4_K_M.gguf" --local-dir "%TARGET_DIR%\llm\lite"

REM Stable Diffusion Modelle
huggingface-cli download SG161222/Realistic_Vision_V6.0 --include "realisticVisionV60B1_v20.safetensors" --local-dir "%TARGET_DIR%\sd"
huggingface-cli download Lykon/DreamShaper --include "dreamshaper_8.safetensors" --local-dir "%TARGET_DIR%\sd"
huggingface-cli download XpucT/Juggernaut-XL-v8 --include "juggernautXL_v8.safetensors" --local-dir "%TARGET_DIR%\sd"
huggingface-cli download ItsJayQz/Flux1-Dev --include "flux1-dev.safetensors" --local-dir "%TARGET_DIR%\sd"
huggingface-cli download stabilityai/stable-diffusion-3-medium --include "sd3_medium.ckpt" --local-dir "%TARGET_DIR%\sd"

echo.
echo 🔁 Fertig! Alle Modelle wurden (hoffentlich) heruntergeladen.
pause
