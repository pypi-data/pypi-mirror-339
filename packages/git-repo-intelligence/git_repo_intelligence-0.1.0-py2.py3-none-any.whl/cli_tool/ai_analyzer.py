"""
AI-powered analysis module for GitHub commit log analyzer.

This module integrates with OpenAI's API to provide enhanced analysis
of commit messages, diffs, and development patterns.
"""

import os
import json
import random
import logging
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Global variable to hold OpenAI client
openai_client = None


def init_openai_client(api_key: Optional[str] = None) -> bool:
    """
    Initialize the OpenAI client.
    
    Args:
        api_key: OpenAI API key (optional, will use environment variable if not provided)
        
    Returns:
        bool: True if initialization successful, False otherwise
    """
    global openai_client
    
    try:
        import openai
        
        # Use provided API key or get from environment
        key = api_key or os.environ.get("OPENAI_API_KEY")
        if not key:
            logger.warning("No OpenAI API key provided. AI analysis will be unavailable.")
            return False
        
        # Initialize client
        openai.api_key = key
        openai_client = openai
        
        logger.info("OpenAI client initialized successfully")
        return True
        
    except ImportError:
        logger.warning("OpenAI package not installed. Please install with: pip install openai")
        return False
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI client: {str(e)}")
        return False


def analyze_with_ai(commit_data: List[Dict[str, Any]], prompt_config: Dict) -> Dict[str, Any]:
    """
    Perform AI-powered analysis on commit data.
    
    Args:
        commit_data: List of commit data dictionaries
        prompt_config: Dictionary containing prompt configurations
        
    Returns:
        Dictionary containing AI analysis results
    """
    default_result = {
        "technical_challenges": "AI analysis unavailable",
        "progression": "AI analysis unavailable",
        "time_consumption": "AI analysis unavailable",
        "comprehensive_report": "AI analysis unavailable"
    }
    
    if not openai_client:
        logger.warning("OpenAI client not initialized. Using fallback analysis.")
        return default_result
    
    try:
        # Create a simplified version of commit data for the prompt
        simplified_data = _simplify_commit_data(commit_data)
        
        # Token estimation (very rough estimate: ~4 chars = 1 token)
        estimated_tokens = len(json.dumps(simplified_data)) // 4
        
        # If the data is too large, further reduce it
        if estimated_tokens > 60000:  # OpenAI has 16k context for GPT-3.5-turbo
            logger.warning(f"Commit data is very large ({estimated_tokens} estimated tokens). Sampling commits to reduce size.")
            simplified_data = _sample_commits_for_analysis(simplified_data)
        
        # Enhanced system prompt for better technical documentation
        system_prompt = """You are a technical documentation AI assistant.
Your goal is to analyze a GitHub repository's commit history, code structure, and discussions (issues, PRs, README, etc.) and generate a professional, clean, and structured report in the style of a technical evolution and summary document.

Output Format:
The report should include the following sections:

Project Overview – Purpose, key features, and intended audience.

Evolution Timeline – Date-wise milestones from commit history or changelog.

Technical Challenges & Solutions – Based on issues/PRs/commits, explain key problems and how they were solved.

Performance Improvements – Quantify where possible (e.g., speed, memory).

Deployment & Usage – CLI, Docker, APIs, etc.

Impact Summary – Summarized benefits/results in tabular format.

Contributors & References – Key contributors, repo links, PR references.

Output Style:
Use markdown with headings, tables, and bullet points.
Use clean, concise, and professional tone.
Avoid fluff, keep it factual and useful.
Include direct references to commits/issues/PRs (e.g., #123, commit abc123)."""

        try:
            # Check available models
            model = "gpt-4-turbo" if _model_is_available("gpt-4-turbo") else "gpt-3.5-turbo"
            
            # Check for comprehensive report prompt
            if "comprehensive_report_prompt" in prompt_config:
                # Use the user's custom prompt
                user_prompt = prompt_config["comprehensive_report_prompt"].format(commit_data=json.dumps(simplified_data, indent=2))
                comprehensive_report = _get_ai_completion(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    max_tokens=3000,
                    model=model
                )
                
                return {
                    "comprehensive_report": comprehensive_report,
                    "technical_challenges": comprehensive_report,
                    "progression": comprehensive_report,
                    "time_consumption": comprehensive_report
                }
            
            # If no comprehensive prompt found, use the default system prompt
            user_prompt = f"Please analyze the following Git commit history and generate a comprehensive technical report:\n\n{json.dumps(simplified_data, indent=2)}"
            comprehensive_report = _get_ai_completion(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_tokens=3000,
                model=model
            )
            
            return {
                "comprehensive_report": comprehensive_report,
                "technical_challenges": comprehensive_report,
                "progression": comprehensive_report,
                "time_consumption": comprehensive_report
            }
            
        except Exception as e:
            if "429" in str(e) or "rate_limit_exceeded" in str(e):
                logger.warning("Rate limit exceeded. Falling back to GPT-3.5-turbo with reduced data.")
                return _handle_rate_limit(system_prompt, simplified_data)
            else:
                raise e
                
    except Exception as e:
        logger.error(f"Error in AI analysis: {str(e)}")
        return {
            "error": str(e),
            "technical_challenges": f"Error in AI analysis: {str(e)}",
            "progression": f"Error in AI analysis: {str(e)}",
            "time_consumption": f"Error in AI analysis: {str(e)}",
            "comprehensive_report": f"Error in AI analysis: {str(e)}"
        }


def _handle_rate_limit(system_prompt: str, simplified_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Handle rate limit by trying with reduced data and GPT-3.5-turbo."""
    # Further reduce data if needed
    reduced_data = _sample_commits_for_analysis(simplified_data, max_commits=50)
    
    try:
        # Try with smaller model and reduced data
        user_prompt = f"Please analyze the following Git commit history and generate a comprehensive technical report (note this is a reduced sample of commits):\n\n{json.dumps(reduced_data, indent=2)}"
        comprehensive_report = _get_ai_completion(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=2000,
            model="gpt-3.5-turbo"
        )
        
        return {
            "comprehensive_report": comprehensive_report,
            "technical_challenges": comprehensive_report,
            "progression": comprehensive_report,
            "time_consumption": comprehensive_report
        }
    except Exception as inner_e:
        logger.error(f"Error in fallback AI analysis: {str(inner_e)}")
        raise inner_e


def _sample_commits_for_analysis(commits: List[Dict[str, Any]], max_commits: int = 100) -> List[Dict[str, Any]]:
    """Sample commits to reduce data size."""
    if len(commits) <= max_commits:
        return commits
        
    # Always keep first and last commit
    sampled_data = [commits[0], commits[-1]]
    
    # Sample the rest
    if len(commits) > 2:
        middle_sample = random.sample(commits[1:-1], min(max_commits - 2, len(commits) - 2))
        sampled_data.extend(middle_sample)
    
    # Sort by date
    sampled_data = sorted(sampled_data, key=lambda x: x.get('date', ''), reverse=True)
    logger.info(f"Reduced to {len(sampled_data)} commits for AI analysis.")
    
    return sampled_data


def _model_is_available(model_name: str) -> bool:
    """
    Check if a specific OpenAI model is available for the current API key.
    
    Args:
        model_name: Name of the model to check
        
    Returns:
        True if the model is available, False otherwise
    """
    try:
        # First, check if we have access to the models list
        models = openai_client.models.list()
        available_models = [model.id for model in models.data]
        return model_name in available_models
    except Exception as e:
        logger.warning(f"Could not check model availability: {str(e)}")
        return False


def _get_ai_completion(system_prompt: str, user_prompt: str, max_tokens: int = 800, model: str = "gpt-3.5-turbo") -> str:
    """
    Get completion from OpenAI API.
    
    Args:
        system_prompt: The system prompt for context
        user_prompt: The user prompt with specific request
        max_tokens: Maximum tokens for the response
        model: OpenAI model to use
        
    Returns:
        The model's response
    """
    try:
        # Use Chat Completions API (GPT models)
        response = openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.2,  # Low temperature for more deterministic responses
        )
        
        # Extract and return the content
        if hasattr(response, 'choices') and len(response.choices) > 0:
            return response.choices[0].message.content
        else:
            return "No response received from AI model."
            
    except Exception as e:
        logger.error(f"Error getting AI completion: {str(e)}")
        raise e  # Re-raise to be handled by the caller


def _simplify_commit_data(commit_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Simplify commit data to reduce token usage.
    
    Args:
        commit_data: Original commit data
        
    Returns:
        Simplified version of commit data
    """
    simplified = []
    
    for commit in commit_data:
        simplified_commit = {
            "hash": commit["short_hash"],
            "date": commit["date"].strftime("%Y-%m-%d %H:%M"),
            "message": commit["message"],
            "author": commit["author"].split('<')[0].strip(),
            "lines_added": commit["stats"]["lines_added"],
            "lines_removed": commit["stats"]["lines_removed"],
            "files_changed": commit["stats"]["files_changed"],
            "file_types": list(commit["stats"]["file_types"].keys()) if "file_types" in commit["stats"] else [],
            "keywords": commit["keywords"]
        }
        
        simplified.append(simplified_commit)
    
    return simplified 