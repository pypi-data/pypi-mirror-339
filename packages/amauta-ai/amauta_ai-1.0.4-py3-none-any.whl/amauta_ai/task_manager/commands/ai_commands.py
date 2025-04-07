"""
AI-assisted task commands for AMAUTA.

This module provides task commands that use AI to enhance their functionality.
"""

import json
import logging
import random
import string
import time
import typer
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich import box
from typing import Any, Dict, List, Optional, Set, Tuple, Annotated, Union

from amauta_ai.ai.service import AiService
from amauta_ai.config.service import ConfigService
from amauta_ai.task_manager.service import TaskManagerService
from amauta_ai.task_manager.models import TaskItem, TaskStatus, TaskPriority, ItemType
from amauta_ai.utils.error_handler import friendly_error
from amauta_ai.utils.console import (
    console,
    confirm_action,
    create_spinner,
    format_id,
    get_priority_icon,
    get_type_icon,
)
from amauta_ai.ai.provider_selection import ProviderMode

# Configure subapp
task_app = typer.Typer(help="Task related commands")

logger = logging.getLogger(__name__)

# Import from the base module
from amauta_ai.task_manager.commands.base import (
    # Imported services
    TaskManagerService,
    
    # Imported models
    ItemType,
    TaskItem,
    TaskPriority,
    TaskStatus,
    
    # Typer apps
    task_app,
    
    # Utilities
    console,
    friendly_error,
    get_status_icon,
    get_priority_icon,
    get_type_icon,
    format_id,
    confirm_action,
    create_spinner,
    get_global_research_flag
)

# Import AI service and config service
from amauta_ai.ai.service import AiService
from amauta_ai.config.service import ConfigService


@task_app.command("add")
@friendly_error("Failed to add task with AI assistance")
def add_task_with_ai(
    prompt: Annotated[
        str, typer.Option("--prompt", "-p", help="Description of the task to create")
    ],
    type: Annotated[
        str,
        typer.Option(help="Type of task to create (task, story, epic, issue)"),
    ] = "task",
    parent: Annotated[
        Optional[str], typer.Option(help="Parent item ID to attach this task to")
    ] = None,
    priority: Annotated[
        str,
        typer.Option(help="Priority of the task (low, medium, high, critical)"),
    ] = "medium",
    research: Annotated[
        bool, typer.Option(help="Use research-optimized provider (Perplexity) for task creation")
    ] = False,
    provider: Annotated[
        Optional[str], typer.Option(help="Explicitly select AI provider (anthropic, perplexity)")
    ] = None,
    offline: Annotated[
        bool, typer.Option(help="Use offline mode with limited AI capabilities")
    ] = False,
) -> None:
    """
    Add a new task with AI assistance.

    This command uses AI to enhance task creation by generating a well-structured
    task description and metadata based on your prompt. It follows the Research-Plan-Execute-Test-Document
    workflow to ensure comprehensive task definition.

    Examples:
      - Create a simple task: amauta task add --prompt="Implement user authentication"
      - Create an epic: amauta task add --prompt="Redesign the dashboard" --type=epic
      - Create with parent: amauta task add --prompt="Add filters" --parent=EPIC-001
      - Use research mode: amauta task add --prompt="Research OAuth security best practices" --research
      - Select provider: amauta task add --prompt="Implement API caching" --provider=anthropic
      - Use offline mode: amauta task add --prompt="Fix responsive layout" --offline
      
    Note: The global --research flag will be used if specified on the main command.
    """
    # Check for global research flag
    research = research or get_global_research_flag()
    
    # Check for global offline flag
    from amauta_ai.main import global_options
    global_offline = getattr(global_options, 'offline', False)
    offline = offline or global_offline
    
    task_service = TaskManagerService()
    
    # Validate parent if specified
    if parent:
        parent_item = task_service.get_item_by_id(parent)
        if not parent_item:
            typer.secho(f"Error: Parent item '{parent}' not found.", fg=typer.colors.RED)
            raise typer.Exit(1)
    
    # Validate type
    try:
        item_type = ItemType(type.title())
    except ValueError:
        valid_types = ", ".join([t.value for t in ItemType])
        typer.secho(
            f"Error: Invalid type '{type}'. Valid values are: {valid_types}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
    # Validate priority
    try:
        item_priority = TaskPriority(priority.lower())
    except ValueError:
        valid_priorities = ", ".join([p.value for p in TaskPriority])
        typer.secho(
            f"Error: Invalid priority '{priority}'. Valid values are: {valid_priorities}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
    # Create Config Service 
    config_service = ConfigService()
    
    # Create AI service with offline mode properly set from the beginning
    ai_service = AiService(config_service, offline_mode=offline)
    
    # Determine required capabilities based on research flag
    required_capabilities = ["task"]
    if research:
        required_capabilities.append("research")
    
    # If we're in offline mode, generate a reasonable default
    if ai_service.is_offline():
        title = prompt[:60] + ("..." if len(prompt) > 60 else "")
        description = f"Task created in offline mode based on: {prompt}\n\n"
        description += "To enable AI assistance:\n"
        description += "1. Ensure you have the required API keys in .env file\n"
        description += "2. Check your internet connection"
        
        # Generate a unique ID for the task
        import random
        import string
        import time
        
        # Generate a simple unique ID using time and random characters
        prefix = item_type.value[0].upper()  # First letter of the type
        timestamp = int(time.time())  # Current timestamp
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        unique_id = f"{prefix}-{timestamp}-{random_suffix}"
        
        # Add the task with the correct method signature
        result_id = task_service.add_item(
            item_type=item_type,
            title=title,
            description=description,
            parent_id=parent,
            priority=item_priority,
            details=f"Task added in offline mode at {time.strftime('%Y-%m-%d %H:%M:%S')}.",
            item_id=unique_id
        ).id
        
        # Display the created task
        created_item = task_service.get_item_by_id(result_id)
        
        typer.secho(f"\nTask created in offline mode: {unique_id}", fg=typer.colors.GREEN)
        return
    
    # Build AI prompt based on task type
    system_prompt = "You are an expert software development task planner that specializes in creating comprehensive, well-structured tasks."
    
    # Enhanced prompt with Research-Plan-Execute-Test-Document workflow
    ai_prompt = f"""
I need to create a new {item_type.value.lower()} in my task management system with the following description:

{prompt}

Please help me generate a well-structured {item_type.value.lower()} following the Research-Plan-Execute-Test-Document workflow.

First, RESEARCH the prompt by analyzing the requirements, gathering relevant context, and identifying best practices.
Then, create a detailed task with:

1. A clear, concise title (max 80 characters)
2. A comprehensive description that explains the task purpose and scope
3. A structured approach that follows the workflow phases:
   - Research: What information needs to be gathered
   - Plan: How the implementation should be approached
   - Execute: Key implementation steps
   - Test: How the implementation should be verified
   - Document: What documentation is needed

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
Title: [title]
Description: [description]
Priority: [low/medium/high/critical]
"""

    # Add context for parent if provided
    if parent:
        parent_item = task_service.get_item_by_id(parent)
        if parent_item:
            ai_prompt += f"""
Parent Information:
- Parent ID: {parent_item.id}
- Parent Title: {parent_item.title}
- Parent Type: {parent_item.type.value}
- Parent Description: {parent_item.description}

Please ensure the new {item_type.value.lower()} aligns with and supports the parent.
"""

    # Generate task details using AI
    with create_spinner("Using AI to generate task details..."):
        try:
            # Call AI service with the selected provider
            result = ai_service.query_task(
                prompt=ai_prompt,
                task_type="create",
                system_prompt=system_prompt,
                provider_name=provider,
                temperature=0.7
            )
            
            # Parse response to extract title, description and priority
            title = ""
            description = ""
            item_priority = TaskPriority.MEDIUM
            
            # Handle the response dictionary from query_task
            if isinstance(result, dict):
                raw_response = result.get("raw_response", "")
                if raw_response:
                    lines = raw_response.strip().split('\n')
                    for line in lines:
                        if line.startswith("Title:"):
                            title = line[len("Title:"):].strip()
                        elif line.startswith("Description:"):
                            description = line[len("Description:"):].strip()
                        elif line.startswith("Priority:"):
                            priority_text = line[len("Priority:"):].strip().lower()
                            # Map priority text to TaskPriority enum
                            priority_map = {
                                "low": TaskPriority.LOW,
                                "medium": TaskPriority.MEDIUM,
                                "high": TaskPriority.HIGH,
                                "critical": TaskPriority.CRITICAL
                            }
                            item_priority = priority_map.get(priority_text, TaskPriority.MEDIUM)
            else:
                # Fallback for string response (older API version compatibility)
                lines = result.strip().split('\n')
                for line in lines:
                    if line.startswith("Title:"):
                        title = line[len("Title:"):].strip()
                    elif line.startswith("Description:"):
                        description = line[len("Description:"):].strip()
                    elif line.startswith("Priority:"):
                        priority_text = line[len("Priority:"):].strip().lower()
                        # Map priority text to TaskPriority enum
                        priority_map = {
                            "low": TaskPriority.LOW,
                            "medium": TaskPriority.MEDIUM,
                            "high": TaskPriority.HIGH,
                            "critical": TaskPriority.CRITICAL
                        }
                        item_priority = priority_map.get(priority_text, TaskPriority.MEDIUM)
            
            # Check if we got meaningful results
            if not title or len(title) < 3:
                typer.secho("Error: AI did not generate a valid title.", fg=typer.colors.RED)
                raise typer.Exit(1)
            
            if not description or len(description) < 10:
                typer.secho("Error: AI did not generate a valid description.", fg=typer.colors.RED)
                raise typer.Exit(1)
            
            # Format description to include workflow structure if not already present
            if "## Research" not in description and "## Plan" not in description:
                description = f"""
{description}

## Workflow
1. **Research**: Gather all necessary information and context
2. **Plan**: Create a detailed implementation plan
3. **Execute**: Implement the solution following best practices
4. **Test**: Verify functionality with appropriate testing
5. **Document**: Document the implementation details and usage
"""

        except Exception as e:
            typer.secho(f"Error generating with AI: {str(e)}", fg=typer.colors.RED)
            typer.secho("Using your prompt as title and description instead.", fg=typer.colors.YELLOW)
            title = prompt[:80] if len(prompt) > 80 else prompt
            description = prompt
    
    # Create the task item
    item = TaskItem(
        id="",  # Will be generated by the service
        title=title,
        description=description,
        type=item_type,
        status=TaskStatus.PENDING,
        priority=item_priority,
        parent=parent,
        subtasks=[],
        dependencies=[],
        dependent_on=[],
        details="",
        metadata={
            "ai_generated": True,
            "prompt": prompt,
        }
    )
    
    # Add the task
    result_id = task_service.add_item(
        item_type=item_type,
        title=title,
        description=description,
        parent_id=parent,
        priority=item_priority,
        details="",
    ).id
    
    # Display the created task
    created_item = task_service.get_item_by_id(result_id)
    if created_item:
        console.print()
        console.print(Panel(
            f"[bold green]Task Created: {format_id(created_item.id)}[/bold green]\n\n"
            f"[bold]{created_item.title}[/bold]\n\n"
            f"{created_item.description}",
            title=f"{get_type_icon(created_item.type)} {created_item.type.value}",
            subtitle=f"{get_priority_icon(created_item.priority)} {created_item.priority.value.capitalize()} Priority",
            expand=False,
            width=100
        ))
        
        # Show parent relationship if any
        if created_item.parent:
            parent_item = task_service.get_item_by_id(created_item.parent)
            if parent_item:
                console.print(f"[dim]Parent: {format_id(parent_item.id)} - {parent_item.title}[/dim]")
        
        console.print()
        typer.secho(
            f"Task added successfully with ID: {created_item.id}",
            fg=typer.colors.GREEN,
        )
    else:
        typer.secho(
            f"Task was created with ID: {result_id}, but could not retrieve it for display.",
            fg=typer.colors.YELLOW,
        )


@task_app.command("update")
@friendly_error("Failed to update task with AI assistance")
def update_task_with_ai(
    id: Annotated[
        str, typer.Argument(help="ID of the task to update")
    ],
    prompt: Annotated[
        str, typer.Option("--prompt", "-p", help="Instructions for updating the task")
    ],
    research: Annotated[
        bool, typer.Option(help="Use research-optimized provider (Perplexity) for task update")
    ] = False,
    provider: Annotated[
        Optional[str], typer.Option(help="Explicitly select AI provider (anthropic, perplexity)")
    ] = None,
    offline: Annotated[
        bool, typer.Option(help="Use offline mode with limited AI capabilities")
    ] = False,
) -> None:
    """
    Update a task with AI assistance.

    This command uses AI to rewrite or enhance an existing task based on your instructions.

    Examples:
      - Update a task: amauta task update TASK-123 --prompt="Add more details about JWT implementation"
      - Use research mode: amauta task update EPIC-456 --prompt="Add best practices for REST API security" --research
      - Select provider: amauta task update STORY-789 --prompt="Update acceptance criteria" --provider=anthropic
      
    Note: The global --research flag will be used if specified on the main command.
    """
    # Check for global research flag
    research = research or get_global_research_flag()
    
    # Check for global offline flag
    from amauta_ai.main import global_options
    global_offline = getattr(global_options, 'offline', False)
    offline = offline or global_offline
    
    task_service = TaskManagerService()
    
    # Verify item exists
    item = task_service.get_item_by_id(id)
    if not item:
        typer.secho(f"Error: Item '{id}' not found.", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    # Create Config Service
    config_service = ConfigService()
    
    # Create AI service with offline mode properly set from the beginning
    ai_service = AiService(config_service, offline_mode=offline)
    
    # If we're in offline mode, generate a reasonable default
    if ai_service.is_offline():
        # Add simple offline update capability
        item.description += f"\n\n[UPDATED IN OFFLINE MODE]: {prompt}"
        item.details += f"\n\nOffline update at {time.strftime('%Y-%m-%d %H:%M:%S')}: {prompt}"
        
        # Save the updated item
        task_service.update_item(item)
        
        typer.secho(f"\nTask {id} updated in offline mode.", fg=typer.colors.GREEN)
        return
    
    # Generate updated task details using AI
    with create_spinner("Using AI to update task details..."):
        try:
            # Construct a prompt for the AI
            ai_prompt = f"""Update the following {item.type.value} based on these instructions: "{prompt}"

            Current {item.type.value} details:
            Title: {item.title}
            Description: {item.description}
            
            Provide an updated version with the following fields:
            1. Title (you can keep it the same if not needed)
            2. Description (improve based on the instructions)
            
            Format your response as JSON with the following fields:
            {{
              "title": "Updated title here",
              "description": "Updated description here"
            }}
            """
            
            # Call AI service with the selected provider
            result = ai_service.query_task(
                prompt=ai_prompt,
                task_type="update",
                system_prompt=f"You are an expert in software development planning, especially in updating {item.type.value}s.",
                provider_name=provider,
                temperature=0.7
            )
            
            # Extract updated task information
            title = result.get("title", item.title)
            description = result.get("description", item.description)

        except Exception as e:
            typer.secho(f"Error generating with AI: {str(e)}", fg=typer.colors.RED)
            typer.secho("No changes will be made to the task.", fg=typer.colors.YELLOW)
            raise typer.Exit(1)
    
    # Preview changes
    console.print("\n[bold]AI-Updated Task:[/bold]")
    
    # Title comparison
    console.print("[bold cyan]Title:[/bold cyan]")
    if title != item.title:
        console.print(f"[red]- {item.title}[/red]")
        console.print(f"[green]+ {title}[/green]")
    else:
        console.print(f"  {title} [dim](unchanged)[/dim]")
    
    # Description comparison
    console.print("\n[bold cyan]Description:[/bold cyan]")
    if description != item.description:
        console.print("[bold]Original:[/bold]")
        console.print(Markdown(item.description or "(empty)"))
        console.print("[bold]Updated:[/bold]")
        console.print(Markdown(description))
    else:
        console.print("  [dim](unchanged)[/dim]")
    
    # Check if there are any changes
    if title == item.title and description == item.description:
        typer.secho("No changes were suggested by AI.", fg=typer.colors.YELLOW)
        return
    
    # Update the item automatically
    item.title = title
    item.description = description
    task_service.update_item(item)
    
    # Show success message
    typer.secho(f"✅ Updated {item.type.value}: {id} - {title}", fg=typer.colors.GREEN)


@task_app.command("expand")
@friendly_error("Failed to expand task with AI assistance")
def expand_task_with_ai(
    id: Annotated[
        str, typer.Argument(help="ID of the task to expand into subtasks")
    ],
    num_subtasks: Annotated[
        int, typer.Option("--num", "-n", help="Number of subtasks to generate")
    ] = 3,
    research: Annotated[
        bool, typer.Option(help="Use research-optimized provider (Perplexity) for task expansion")
    ] = False,
    provider: Annotated[
        Optional[str], typer.Option(help="Explicitly select AI provider (anthropic, perplexity)")
    ] = None,
    offline: Annotated[
        bool, typer.Option(help="Use offline mode with limited AI capabilities")
    ] = False,
) -> None:
    """
    Expand a task into more detailed subtasks with AI assistance.

    This command uses AI to break down a task into smaller, more manageable subtasks.
    It analyzes the task description and generates a set of well-structured subtasks
    that collectively accomplish the parent task.

    Examples:
      - Expand a task: amauta task expand TASK-123
      - Generate more subtasks: amauta task expand TASK-123 --num 5
      - Use research mode: amauta task expand TASK-123 --research
      - Select provider: amauta task expand TASK-123 --provider=anthropic
    """
    # Check for global research flag
    research = research or get_global_research_flag()
    
    # Check for global offline flag
    from amauta_ai.main import global_options
    global_offline = getattr(global_options, 'offline', False)
    offline = offline or global_offline
    
    task_service = TaskManagerService()
    
    # Validate task exists
    task = task_service.get_item_by_id(id)
    if not task:
        typer.secho(f"Error: Task '{id}' not found.", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    # Create Config Service
    config_service = ConfigService()
    
    # Create AI service with offline mode properly set from the beginning
    ai_service = AiService(config_service, offline_mode=offline)
    
    # If we're in offline mode, generate a reasonable default
    if ai_service.is_offline():
        typer.secho(
            f"\nError: Task expansion requires AI capabilities that are not available in offline mode.",
            fg=typer.colors.RED,
        )
        typer.secho(
            "Please ensure you have the required API keys configured and an internet connection.",
            fg=typer.colors.YELLOW,
        )
        raise typer.Exit(1)
    
    # Gather task context
    context = task_service.get_task_context(id)
    
    # Initialize complexity analysis results
    complexity_analysis = None
    complexity_score = None
    
    # Step 1: If research flag is enabled, perform complexity analysis first
    if research:
        with create_spinner(f"Analyzing task complexity using research provider..."):
            try:
                # Use analyze_complexity function from this module
                # We'll call it directly rather than via CLI to get the results
                
                # First create the prompt for complexity analysis
                complexity_prompt = f"""
You are analyzing the complexity of a task in a project management system.

Task details:
- ID: {task.id}
- Title: {task.title}
- Type: {task.type.value}
- Description: {task.description}

Please analyze this task and evaluate its complexity. Consider the following aspects:
1. Technical complexity 
2. Domain knowledge required
3. Dependencies and interactions
4. Time required to implement
5. Potential risks

Provide an overall complexity score on a scale of 1-10, where:
1-3 = Simple task, straightforward implementation
4-6 = Moderate complexity, requires some planning
7-8 = High complexity, requires careful planning and expertise
9-10 = Very high complexity, may need to be broken down further

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
Complexity Score: [NUMBER]
Analysis:
[Your detailed analysis here explaining the score and aspects considered]
Required Skills:
[List of technical skills or domain knowledge needed]
Estimated Time:
[Estimated time to complete in hours/days]
Suggested Breakdown:
[High-level suggestion on how many subtasks this should be broken into]
"""
                
                # Use the research-optimized provider for complexity analysis
                complexity_response = ai_service.query_llm(
                    prompt=complexity_prompt,
                    provider=provider,  # May be None, in which case the service selects based on mode
                    mode=ProviderMode.ANALYSIS,
                    research=True,  # Force research mode for complexity analysis
                )
                
                # Parse the complexity score and analysis
                # Handle the response which might be a string or a dictionary
                complexity_analysis = ""
                if isinstance(complexity_response, dict):
                    complexity_analysis = complexity_response.get("raw_response", "")
                else:
                    complexity_analysis = complexity_response.strip()
                
                # Try to extract the complexity score
                import re
                score_match = re.search(r"Complexity Score:\s*(\d+(?:\.\d+)?)", complexity_analysis)
                if score_match:
                    complexity_score = float(score_match.group(1))
                    typer.secho(f"Complexity analysis completed. Score: {complexity_score}/10", fg=typer.colors.BLUE)
                else:
                    typer.secho("Complexity score could not be extracted from the analysis.", fg=typer.colors.YELLOW)
            
            except Exception as e:
                typer.secho(f"Error during complexity analysis: {str(e)}", fg=typer.colors.YELLOW)
                typer.secho("Proceeding with task expansion without complexity analysis.", fg=typer.colors.YELLOW)
    
    # Step 2: Generate subtasks
    with create_spinner(f"Using AI to expand task {id} into {num_subtasks} subtasks..."):
        # Construct a prompt for the AI
        # If we have complexity analysis, include it in the prompt
        if complexity_analysis:
            prompt = f"""
You are breaking down a task in a project management system into smaller subtasks following the Research-Plan-Execute-Test-Document workflow. 
We have performed a complexity analysis that you should use to guide your breakdown.

TASK DETAILS:
- ID: {task.id}
- Title: {task.title}
- Type: {task.type.value}
- Description: {task.description}

COMPLEXITY ANALYSIS:
{complexity_analysis}

Based on this complexity analysis, please break down this task into exactly {num_subtasks} subtasks following the Research-Plan-Execute-Test-Document workflow:

1. RESEARCH subtasks: Focus on gathering information, requirements analysis, and context understanding
2. PLAN subtasks: Focus on designing solutions, architecture, and implementation planning
3. EXECUTE subtasks: Focus on actual implementation and coding
4. TEST subtasks: Focus on validation, testing, and quality assurance
5. DOCUMENT subtasks: Focus on documentation, knowledge sharing, and user guides

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
[SUBTASK]
Title: [Phase] - [Short, descriptive title]
Description: [Detailed description of what this subtask involves]
Priority: [low/medium/high/critical]
Phase: [Research/Plan/Execute/Test/Document]
[END SUBTASK]

[SUBTASK]
...and so on for each subtask
[END SUBTASK]

IMPORTANT GUIDELINES:
1. Create exactly {num_subtasks} subtasks
2. Make each subtask clear, specific and actionable
3. Distribute the work evenly across the 5 workflow phases
4. Order subtasks logically to follow the workflow progression 
5. Include at least one subtask for each of the 5 phases
6. Subtasks should be ordered by phase: Research first, then Plan, Execute, Test, and Document last
"""
        else:
            # Regular prompt without complexity analysis
            prompt = f"""
You are breaking down a task in a project management system into smaller subtasks following the Research-Plan-Execute-Test-Document workflow.

TASK DETAILS:
- ID: {task.id}
- Title: {task.title}
- Type: {task.type.value}
- Description: {task.description}

Please break down this task into exactly {num_subtasks} subtasks following the Research-Plan-Execute-Test-Document workflow:

1. RESEARCH subtasks: Focus on gathering information, requirements analysis, and context understanding
2. PLAN subtasks: Focus on designing solutions, architecture, and implementation planning
3. EXECUTE subtasks: Focus on actual implementation and coding
4. TEST subtasks: Focus on validation, testing, and quality assurance
5. DOCUMENT subtasks: Focus on documentation, knowledge sharing, and user guides

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
[SUBTASK]
Title: [Phase] - [Short, descriptive title]
Description: [Detailed description of what this subtask involves]
Priority: [low/medium/high/critical]
Phase: [Research/Plan/Execute/Test/Document]
[END SUBTASK]

[SUBTASK]
...and so on for each subtask
[END SUBTASK]

IMPORTANT GUIDELINES:
1. Create exactly {num_subtasks} subtasks
2. Make each subtask clear, specific and actionable
3. Distribute the work evenly across the 5 workflow phases
4. Order subtasks logically to follow the workflow progression
5. Include at least one subtask for each of the 5 phases
6. Subtasks should be ordered by phase: Research first, then Plan, Execute, Test, and Document last
"""
        
        # Generate the subtasks using AI
        response = ai_service.query_llm(
            prompt=prompt,
            provider=provider,
            mode=ProviderMode.TASK,
            research=research,
        )
        
        # Parse the subtasks from the response
        subtasks = []
        current_subtask = None
        subtask_data = {}
        
        # Handle the response which might be a string or a dictionary
        response_text = ""
        if isinstance(response, dict):
            response_text = response.get("raw_response", "")
        else:
            response_text = response
            
        for line in response_text.strip().split('\n'):
            line = line.strip()
            
            if line == "[SUBTASK]":
                # Start a new subtask
                subtask_data = {}
                continue
                
            if line == "[END SUBTASK]":
                # End current subtask and add to list
                if subtask_data and "Title" in subtask_data and "Description" in subtask_data:
                    subtasks.append(subtask_data)
                continue
                
            # Extract fields from the line
            if ":" in line:
                key, value = line.split(":", 1)
                subtask_data[key.strip()] = value.strip()
        
        # Validate we got the requested number of subtasks
        if len(subtasks) < 1:
            typer.secho("Error: AI didn't generate any valid subtasks.", fg=typer.colors.RED)
            raise typer.Exit(1)
        
        if len(subtasks) != num_subtasks:
            typer.secho(
                f"Warning: AI generated {len(subtasks)} subtasks, instead of the requested {num_subtasks}.",
                fg=typer.colors.YELLOW,
            )
    
    # Create the subtasks in the task system
    with create_spinner(f"Creating {len(subtasks)} subtasks for {id}..."):
        created_ids = []
        phase_to_tasks = {
            "research": [],
            "plan": [],
            "execute": [],
            "test": [],
            "document": []
        }
        
        for i, subtask in enumerate(subtasks[:num_subtasks]):
            title = subtask.get("Title", f"Subtask {i+1}")
            description = subtask.get("Description", "")
            priority_str = subtask.get("Priority", "medium").lower()
            details = subtask.get("Details", "")
            phase = subtask.get("Phase", "").lower()
            
            # Make sure phase is one of the valid values
            if phase not in phase_to_tasks:
                phase = "execute"  # Default to execute if not specified
            
            # Map priority string to enum
            try:
                priority = TaskPriority(priority_str)
            except ValueError:
                priority = TaskPriority.MEDIUM
            
            # Create the subtask
            try:
                # For task type, use one level down from parent task type, or default to TASK
                if task.type == ItemType.EPIC:
                    subtask_type = ItemType.TASK
                elif task.type == ItemType.TASK:
                    subtask_type = ItemType.STORY
                elif task.type == ItemType.STORY:
                    subtask_type = ItemType.ISSUE
                else:
                    subtask_type = ItemType.TASK
                
                # Add the subtask
                result = task_service.add_item(
                    item_type=subtask_type,
                    title=title,
                    description=description,
                    parent_id=id,
                    priority=priority,
                    details=details,
                )
                
                # Store the new task ID and map it to its phase
                created_ids.append(result.id)
                phase_to_tasks[phase].append(result.id)
                
            except Exception as e:
                typer.secho(f"Error creating subtask {i}: {str(e)}", fg=typer.colors.RED)
        
        # Establish dependencies between tasks based on phase progression
        phase_order = ["research", "plan", "execute", "test", "document"]
        
        # For each task, add dependencies from all tasks in previous phases
        for i, current_phase in enumerate(phase_order):
            if i == 0:
                continue  # Skip the first phase (Research) as it has no dependencies
                
            # Get all tasks from previous phases
            dependencies = []
            for prev_phase in phase_order[:i]:
                dependencies.extend(phase_to_tasks[prev_phase])
                
            # Add dependencies to all tasks in current phase
            for task_id in phase_to_tasks[current_phase]:
                for dep_id in dependencies:
                    try:
                        task_service.add_dependency(task_id, dep_id)
                    except Exception as e:
                        typer.secho(f"Warning: Could not add dependency {dep_id} to {task_id}: {str(e)}", fg=typer.colors.YELLOW)
    
    # Success message
    if complexity_score:
        typer.secho(
            f"\nSuccessfully expanded task {id} (complexity: {complexity_score}/10) into {len(created_ids)} subtasks:",
            fg=typer.colors.GREEN,
        )
    else:
        typer.secho(
            f"\nSuccessfully expanded task {id} into {len(created_ids)} subtasks:",
            fg=typer.colors.GREEN,
        )
    
    for task_id in created_ids:
        task_item = task_service.get_item_by_id(task_id)
        deps = ", ".join(task_item.dependencies) if task_item.dependencies else "-"
        typer.secho(f"  - {task_id} - {task_item.title} [Dependencies: {deps}]", fg=typer.colors.BLUE)
    
    # Add workflow description
    typer.secho(
        "\nTasks follow the Research-Plan-Execute-Test-Document workflow for optimal implementation.",
        fg=typer.colors.GREEN,
    )
    typer.secho(
        "Dependencies were automatically established between phases to ensure logical progression.",
        fg=typer.colors.GREEN,
    )
    
    # Reminder to update task status
    typer.secho(
        f"\nReminder: Set the parent task {id} to 'in-progress' with 'amauta task set-status {id} in-progress'",
        fg=typer.colors.YELLOW,
    )


@task_app.command("analyze-complexity")
@friendly_error("Failed to analyze complexity")
def analyze_complexity(
    id: Annotated[
        Optional[str], typer.Argument(help="ID of the task to analyze")
    ] = None,
    all: Annotated[
        bool, typer.Option("--all", help="Analyze all tasks")
    ] = False,
    research: Annotated[
        bool, typer.Option(help="Use research-optimized provider (Perplexity) for complexity analysis")
    ] = False,
    provider: Annotated[
        Optional[str], typer.Option(help="Explicitly select AI provider (anthropic, perplexity)")
    ] = None,
    offline: Annotated[
        bool, typer.Option(help="Use offline mode with limited AI capabilities")
    ] = False,
) -> None:
    """
    Analyze the complexity of tasks using AI.

    This command uses AI to assess the complexity of tasks and provide insights
    to help with planning and resource allocation.

    Examples:
      - Analyze a single task: amauta task analyze-complexity TASK-123
      - Analyze all tasks: amauta task analyze-complexity --all
      - Use research mode: amauta task analyze-complexity TASK-123 --research
      - Select provider: amauta task analyze-complexity TASK-123 --provider=anthropic
    """
    # Check for global research flag
    research = research or get_global_research_flag()
    
    # Check for global offline flag
    from amauta_ai.main import global_options
    global_offline = getattr(global_options, 'offline', False)
    offline = offline or global_offline
    
    # Create the service instances
    task_service = TaskManagerService()
    config_service = ConfigService()
    
    # Create AI service with offline mode properly set from the beginning
    ai_service = AiService(config_service, offline_mode=offline)
    
    # If we're in offline mode, show a message
    if ai_service.is_offline():
        typer.secho(
            f"\nError: Complexity analysis requires AI capabilities that are not available in offline mode.",
            fg=typer.colors.RED,
        )
        typer.secho(
            "Please ensure you have the required API keys configured and an internet connection.",
            fg=typer.colors.YELLOW,
        )
        raise typer.Exit(1)
    
    # If neither id nor all is specified, default to analyzing all tasks
    if not id and not all:
        all = True
        typer.secho(
            "No task ID provided, analyzing all tasks. Use --all flag explicitly in the future.",
            fg=typer.colors.YELLOW,
        )
    
    # Get tasks to analyze
    items_to_analyze = []
    if all:
        items_to_analyze = task_service.get_all_items()
    elif id:
        item = task_service.get_item_by_id(id)
        if not item:
            typer.secho(f"Error: Item '{id}' not found.", fg=typer.colors.RED)
            raise typer.Exit(1)
        items_to_analyze = [item]
    
    # Analyze each task
    with create_spinner(f"Analyzing complexity of {len(items_to_analyze)} tasks..."):
        for item in items_to_analyze:
            # Skip items that already have complexity metadata
            if item.metadata and "complexity" in item.metadata:
                continue
            
            try:
                # Prepare item details for analysis
                item_details = {
                    "id": item.id,
                    "title": item.title,
                    "description": item.description,
                    "type": item.type.value,
                }
                
                # Construct prompt for complexity analysis
                prompt = f"""
                Analyze the complexity of the following task:
                
                ID: {item.id}
                Title: {item.title}
                Type: {item.type.value}
                Description: {item.description}
                
                Provide a complexity assessment with:
                1. Complexity score (1-10, where 1 is very simple and 10 is extremely complex)
                2. Estimated effort in person-hours
                3. Brief justification for your assessment
                4. Key factors contributing to complexity
                
                Format your response as JSON:
                {{
                  "complexity_score": 5,
                  "estimated_hours": 8,
                  "justification": "Brief explanation of your assessment",
                  "key_factors": ["Factor 1", "Factor 2", "Factor 3"]
                }}
                """
                
                # Call AI service with selected provider
                result = ai_service.query_task(
                    prompt=prompt,
                    task_type="analysis",
                    system_prompt=f"You are an expert in software development planning, especially in analyzing {item.type.value}s.",
                    provider_name=provider,
                    temperature=0.7
                )
                
                # Parse response
                try:
                    complexity_data = result
                    
                    # Validate complexity_score exists and is between 1-10
                    if "complexity_score" not in complexity_data:
                        complexity_data["complexity_score"] = 5  # Default value
                    else:
                        score = complexity_data["complexity_score"]
                        if not isinstance(score, (int, float)) or score < 1 or score > 10:
                            complexity_data["complexity_score"] = 5  # Default if invalid
                    
                    # Ensure other fields exist with defaults if missing
                    if "estimated_hours" not in complexity_data:
                        complexity_data["estimated_hours"] = complexity_data["complexity_score"] * 2
                    if "justification" not in complexity_data:
                        complexity_data["justification"] = "Automated assessment"
                    if "key_factors" not in complexity_data:
                        complexity_data["key_factors"] = ["Task scope", "Technical requirements"]
                    
                    # Initialize metadata dictionary if it doesn't exist
                    if not item.metadata:
                        item.metadata = {}
                    
                    # Store complexity data in task metadata
                    item.metadata["complexity"] = complexity_data
                    
                    # Update the item
                    task_service.update_item(item)
                    
                except json.JSONDecodeError:
                    typer.secho(f"Error parsing complexity analysis for {item.id}", fg=typer.colors.YELLOW)
                    continue
                
            except Exception as e:
                typer.secho(f"Error analyzing {item.id}: {str(e)}", fg=typer.colors.YELLOW)
                continue
    
    # Display results
    console.print("\n[bold]Complexity Analysis Results:[/bold]")
    
    table = Table(box=box.ROUNDED)
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="bright_white")
    table.add_column("Score", style="yellow")
    table.add_column("Hours", style="green")
    table.add_column("Key Factors", style="bright_blue")
    
    for item in items_to_analyze:
        if not item.metadata or "complexity" not in item.metadata:
            continue
        
        complexity = item.metadata["complexity"]
        score = complexity.get("complexity_score", "-")
        hours = complexity.get("estimated_hours", "-")
        factors = ", ".join(complexity.get("key_factors", [])[:2])  # Show at most 2 factors
        
        table.add_row(
            item.id,
            item.title[:40] + ("..." if len(item.title) > 40 else ""),
            str(score),
            str(hours),
            factors[:60] + ("..." if len(factors) > 60 else "")
        )
    
    console.print(table)
    
    typer.secho(
        f"✅ Analyzed complexity for {len(items_to_analyze)} tasks",
        fg=typer.colors.GREEN,
    )


@task_app.command("generate-tasks")
@friendly_error("Failed to generate tasks with AI")
def generate_tasks_from_prompt(
    prompt: Annotated[
        str, typer.Argument(help="Description of the project or feature to generate tasks for")
    ],
    num_tasks: Annotated[
        int, typer.Option("--num", "-n", help="Number of tasks to generate")
    ] = 5,
    parent: Annotated[
        Optional[str], typer.Option(help="Parent item ID to attach generated tasks to")
    ] = None,
    create: Annotated[
        bool, typer.Option(help="Create the tasks immediately instead of just previewing")
    ] = False,
    research: Annotated[
        bool, typer.Option(help="Use research-optimized provider (Perplexity) for task generation")
    ] = False,
    provider: Annotated[
        Optional[str], typer.Option(help="Explicitly select AI provider (anthropic, perplexity)")
    ] = None,
    offline: Annotated[
        bool, typer.Option(help="Use offline mode with limited AI capabilities")
    ] = False,
) -> None:
    """
    Generate multiple tasks from a prompt with AI assistance.

    This command uses AI to generate a set of tasks for a project or feature based on your description.
    Tasks follow the Research-Plan-Execute-Test-Document workflow for comprehensive implementation.

    Examples:
      - Generate tasks: amauta task generate-tasks "Create a new user authentication system"
      - Specify number of tasks: amauta task generate-tasks "Build an analytics dashboard" --num 10
      - Create tasks immediately: amauta task generate-tasks "API rate limiting" --create
      - Use research mode: amauta task generate-tasks "Implement OAuth 2.0" --research
      - Select provider: amauta task generate-tasks "Deploy to AWS" --provider=anthropic
      
    Note: The global --research flag will be used if specified on the main command.
    """
    # Check for global research flag
    research = research or get_global_research_flag()
    
    # Check for global offline flag
    from amauta_ai.main import global_options
    global_offline = getattr(global_options, 'offline', False)
    offline = offline or global_offline
    
    task_service = TaskManagerService()
    
    # Validate parent if specified
    parent_item = None
    if parent:
        parent_item = task_service.get_item_by_id(parent)
        if not parent_item:
            typer.secho(f"Parent item {parent} not found.", fg=typer.colors.RED)
            raise typer.Exit(1)
    
    # Create Config Service
    config_service = ConfigService()
    
    # Create AI service with offline mode properly set from the beginning
    ai_service = AiService(config_service, offline_mode=offline)
    
    # If we're in offline mode, generate a reasonable default
    if ai_service.is_offline():
        typer.secho(
            f"\nError: Task generation requires AI capabilities that are not available in offline mode.",
            fg=typer.colors.RED,
        )
        typer.secho(
            "Please ensure you have the required API keys configured and an internet connection.",
            fg=typer.colors.YELLOW,
        )
        raise typer.Exit(1)
    
    # Generate tasks using AI
    with create_spinner(f"Using AI to generate {num_tasks} tasks for: {prompt}"):
        # Construct a prompt for the AI
        ai_prompt = f"""
Generate a set of {num_tasks} tasks to implement this feature or project: "{prompt}"

Follow the Research-Plan-Execute-Test-Document workflow to ensure comprehensive implementation:
1. Start with Research tasks to gather information and context
2. Follow with Planning tasks to design the implementation
3. Include Execution tasks for actual implementation
4. Add Testing tasks to verify functionality
5. End with Documentation tasks

For each task, provide:
1. A clear, concise title that includes the workflow phase (e.g., "Research - Investigate authentication options")
2. A detailed description of what needs to be done
3. A priority level (low, medium, high, or critical)
4. The workflow phase it belongs to (Research, Plan, Execute, Test, or Document)

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
[TASK]
Title: [Phase] - [Short, descriptive title]
Description: [Detailed description]
Priority: [low/medium/high/critical]
Phase: [Research/Plan/Execute/Test/Document]
[END TASK]

[TASK]
...and so on for each task
[END TASK]

IMPORTANT GUIDELINES:
1. Create exactly {num_tasks} tasks
2. Make each task clear, specific and actionable
3. Distribute tasks across all 5 workflow phases
4. Order tasks logically to follow the workflow progression
5. Include at least one task for each workflow phase
"""

        # Add parent context if present
        if parent_item:
            ai_prompt += f"""
Parent Task Information:
- ID: {parent_item.id}
- Title: {parent_item.title}
- Type: {parent_item.type.value}
- Description: {parent_item.description}

Ensure generated tasks align with and support this parent task.
"""
        
        # Generate the tasks using AI
        try:
            response = ai_service.query_llm(
                prompt=ai_prompt,
                provider=provider,
                mode=ProviderMode.TASK,
                research=research,
            )
        except Exception as e:
            typer.secho(f"Error generating tasks: {str(e)}", fg=typer.colors.RED)
            raise typer.Exit(1)
        
        # Parse the tasks from the response
        tasks = []
        task_data = {}
        
        for line in response.strip().split('\n'):
            line = line.strip()
            
            if line == "[TASK]":
                # Start a new task
                task_data = {}
                continue
                
            if line == "[END TASK]":
                # End current task and add to list
                if task_data and "Title" in task_data and "Description" in task_data:
                    tasks.append(task_data)
                continue
                
            # Extract fields from the line
            if ":" in line:
                key, value = line.split(":", 1)
                task_data[key.strip()] = value.strip()
    
    # Display the generated tasks
    if not tasks:
        typer.secho("Error: No valid tasks were generated.", fg=typer.colors.RED)
        raise typer.Exit(1)
        
    console.print(f"\n[bold]Generated {len(tasks)} tasks for: {prompt}[/bold]\n")
    
    # Group tasks by phase
    tasks_by_phase = {}
    for task in tasks:
        phase = task.get("Phase", "Unspecified")
        if phase not in tasks_by_phase:
            tasks_by_phase[phase] = []
        tasks_by_phase[phase].append(task)
    
    # Display tasks grouped by workflow phase
    for phase in ["Research", "Plan", "Execute", "Test", "Document"]:
        if phase in tasks_by_phase:
            console.print(f"[bold blue]{phase} Phase:[/bold blue]")
            for i, task in enumerate(tasks_by_phase[phase], 1):
                console.print(Panel(
                    f"[bold]{task.get('Title', f'Task {i}')}" + 
                    (f" [dim]({task.get('Priority', 'medium')})[/dim]" if "Priority" in task else "") + 
                    f"[/bold]\n\n{task.get('Description', 'No description provided')}",
                    expand=False,
                ))
            console.print()
    
    # Create tasks if requested
    created_ids = []
    if create:
        with create_spinner(f"Creating {len(tasks)} tasks..."):
            for task in tasks:
                title = task.get("Title", "Untitled Task")
                description = task.get("Description", "")
                priority_text = task.get("Priority", "medium").lower()
                phase = task.get("Phase", "")
                
                # Map priority text to TaskPriority enum
                priority_map = {
                    "low": TaskPriority.LOW,
                    "medium": TaskPriority.MEDIUM,
                    "high": TaskPriority.HIGH,
                    "critical": TaskPriority.CRITICAL
                }
                priority = priority_map.get(priority_text, TaskPriority.MEDIUM)
                
                # Create a details section with phase info if not in description
                details = ""
                if phase and phase not in description:
                    details = f"## Workflow Phase: {phase}\n\n"
                    
                    # Add phase-specific guidance
                    if phase.lower() == "research":
                        details += "- Conduct thorough research before proceeding\n"
                        details += "- Document all findings for reference\n"
                        details += "- Identify potential challenges and constraints\n"
                    elif phase.lower() == "plan":
                        details += "- Create a detailed implementation plan\n"
                        details += "- Consider alternative approaches\n"
                        details += "- Identify dependencies and risks\n"
                    elif phase.lower() == "execute":
                        details += "- Follow established coding standards\n"
                        details += "- Regularly commit changes\n"
                        details += "- Consider performance and security\n"
                    elif phase.lower() == "test":
                        details += "- Write appropriate tests (unit, integration, etc.)\n"
                        details += "- Verify edge cases and error handling\n"
                        details += "- Document test results\n"
                    elif phase.lower() == "document":
                        details += "- Create clear and concise documentation\n"
                        details += "- Include usage examples\n"
                        details += "- Update relevant project documentation\n"
                
                # Add the task
                try:
                    result = task_service.add_item(
                        item_type=ItemType.TASK,
                        title=title,
                        description=description,
                        parent_id=parent,
                        priority=priority,
                        details=details,
                    )
                    
                    created_ids.append(result.id)
                    
                except Exception as e:
                    typer.secho(f"Error creating task: {str(e)}", fg=typer.colors.RED)
        
        # Success message for created tasks
        if created_ids:
            typer.secho(
                f"\n✓ Successfully created {len(created_ids)} tasks:",
                fg=typer.colors.GREEN,
            )
            
            for task_id in created_ids:
                task_item = task_service.get_item_by_id(task_id)
                typer.secho(f"  - {task_id} - {task_item.title}", fg=typer.colors.BLUE)
                
            # Add workflow reminder
            typer.secho(
                "\nTasks follow the Research-Plan-Execute-Test-Document workflow for comprehensive implementation.",
                fg=typer.colors.GREEN,
            )
    else:
        typer.secho(
            "\nTo create these tasks, run the command again with the --create flag.",
            fg=typer.colors.YELLOW,
        )


@task_app.command("update-cascade")
@friendly_error("Failed to update task and dependencies with AI assistance")
def update_task_cascade_with_ai(
    id: Annotated[
        str, typer.Argument(help="ID of the task to update")
    ],
    prompt: Annotated[
        str, typer.Option("--prompt", "-p", help="Instructions for updating the task")
    ],
    research: Annotated[
        bool, typer.Option(help="Use research-optimized provider (Perplexity) for task update analysis")
    ] = False,
    provider: Annotated[
        Optional[str], typer.Option(help="Explicitly select AI provider (anthropic, perplexity)")
    ] = None,
    preview: Annotated[
        bool, typer.Option(help="Preview changes without applying them")
    ] = False,
    offline: Annotated[
        bool, typer.Option(help="Use offline mode with limited AI capabilities")
    ] = False,
) -> None:
    """
    Update a task and all its dependent tasks to maintain consistency.

    This command uses AI to update a task and analyze the impact on dependent tasks,
    then suggests updates to keep the task hierarchy consistent. This ensures that
    changes to one task are properly propagated to all affected tasks.

    Examples:
      - Update a task and its dependencies: amauta task update-cascade TASK-123 --prompt="Change authentication from JWT to OAuth"
      - Preview changes without applying: amauta task update-cascade TASK-123 --prompt="Modify API endpoint format" --preview
      - Use research mode: amauta task update-cascade TASK-123 --prompt="Update to use GraphQL" --research
    """
    # Check for global research flag
    research = research or get_global_research_flag()
    
    # Check for global offline flag
    from amauta_ai.main import global_options
    global_offline = getattr(global_options, 'offline', False)
    offline = offline or global_offline
    
    task_service = TaskManagerService()
    
    # Validate task exists
    task = task_service.get_item_by_id(id)
    if not task:
        typer.secho(f"Error: Task '{id}' not found.", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    # Create Config Service
    config_service = ConfigService()
    
    # Create AI service with offline mode properly set from the beginning
    ai_service = AiService(config_service, offline_mode=offline)
    
    # Determine required capabilities based on research flag
    required_capabilities = ["task"]
    if research:
        required_capabilities.append("research")
    
    # If we're in offline mode, show an error message
    if ai_service.is_offline():
        typer.secho(
            f"\nError: The update-cascade command requires AI capabilities that are not available in offline mode.",
            fg=typer.colors.RED,
        )
        typer.secho(
            "Please ensure you have the required API keys configured and an internet connection.",
            fg=typer.colors.YELLOW,
        )
        raise typer.Exit(1)
    
    # Step 1: Find all dependent tasks (direct and indirect)
    with create_spinner("Identifying dependent tasks..."):
        # Get all tasks that depend on the specified task
        all_items = task_service.get_all_items()
        dependent_tasks = []
        
        def find_all_dependent_tasks(task_id, visited=None):
            if visited is None:
                visited = set()
            
            if task_id in visited:
                return
            
            visited.add(task_id)
            
            # Find direct dependencies
            direct_dependents = [item for item in all_items if task_id in item.dependencies]
            for dependent in direct_dependents:
                dependent_tasks.append(dependent)
                # Recurse to find indirect dependencies
                find_all_dependent_tasks(dependent.id, visited)
        
        # Start with the task we're updating
        find_all_dependent_tasks(id)
    
    # If no dependent tasks, inform user
    if not dependent_tasks:
        typer.secho(f"\nNo dependent tasks found for {id}. Using regular update instead.", fg=typer.colors.YELLOW)
        
        # Call the regular update command
        update_task_with_ai(id=id, prompt=prompt, research=research, provider=provider, offline=offline)
        return
    
    # Step 2: Generate update for the main task
    with create_spinner(f"Using AI to update task {id}..."):
        task_context = task_service.get_task_context(id)
        
        # Construct a prompt for the AI to update the main task
        main_prompt = f"""
You are updating a task in a project management system. 
Task details:
- ID: {task.id}
- Title: {task.title}
- Type: {task.type.value}
- Status: {task.status.value}
- Priority: {task.priority.value}
- Current description: {task.description}

Update instructions: {prompt}

For the response, please provide:
1. An updated title (keep it concise)
2. An updated description (be thorough but clear)
"""
        
        # Use AI to generate the update
        main_response = ai_service.query_llm(
            prompt=main_prompt,
            provider=provider,
            mode=ProviderMode.TASK,
            research=research,
        )
        
        # Parse the response
        try:
            lines = main_response.strip().split("\n")
            updated_title = lines[0].strip()
            updated_description = "\n".join(lines[1:]).strip()
            
            # Create updated task object
            updated_task = task.model_copy(deep=True)
            updated_task.title = updated_title
            updated_task.description = updated_description
        except Exception as e:
            typer.secho(f"Error parsing AI response: {str(e)}", fg=typer.colors.RED)
            typer.secho("Please try a different prompt or contact support.", fg=typer.colors.YELLOW)
            raise typer.Exit(1)
    
    # Step 3: Generate updates for dependent tasks
    dependent_updates = []
    
    with create_spinner(f"Analyzing dependencies and generating consistent updates..."):
        for dependent_task in dependent_tasks:
            # Construct context for this task including:
            # - The task itself
            # - Its relationship to the parent task
            # - The changes being made to the parent
            
            cascade_prompt = f"""
You are updating a task that depends on another task that has just been modified.
We need to maintain consistency across related tasks.

ORIGINAL PARENT TASK:
- ID: {task.id}
- Title: {task.title}
- Description: {task.description}

UPDATED PARENT TASK:
- ID: {task.id}
- Title: {updated_task.title}
- Description: {updated_task.description}

DEPENDENT TASK (NEEDS UPDATE):
- ID: {dependent_task.id}
- Title: {dependent_task.title}
- Description: {dependent_task.description}

This dependent task relies on the parent task that was just updated. The parent task was updated with these instructions: "{prompt}"

Please provide consistent updates for the dependent task to ensure it remains aligned with the updated parent task.
For the response, please provide:
1. An updated title for the dependent task (keep it concise)
2. An updated description for the dependent task (be thorough but clear)
"""
            
            # Generate the consistent update for this dependent task
            cascade_response = ai_service.query_llm(
                prompt=cascade_prompt,
                provider=provider,
                mode=ProviderMode.TASK,
                research=research,
            )
            
            # Parse the response
            try:
                lines = cascade_response.strip().split("\n")
                dep_updated_title = lines[0].strip()
                dep_updated_description = "\n".join(lines[1:]).strip()
                
                updated_dependent = dependent_task.model_copy(deep=True)
                updated_dependent.title = dep_updated_title
                updated_dependent.description = dep_updated_description
                
                dependent_updates.append((dependent_task, updated_dependent))
            except Exception as e:
                typer.secho(f"Error generating update for {dependent_task.id}: {str(e)}", fg=typer.colors.YELLOW)
                typer.secho("Skipping this dependent task.", fg=typer.colors.YELLOW)
                continue
    
    # Step 4: Preview the changes
    console.print("\n[bold]Proposed Updates:[/bold]")
    
    # Show main task update
    console.print(f"\n[bold]Main Task ([cyan]{task.id}[/cyan]):[/bold]")
    
    # Create a table to display the before/after
    main_table = Table(title=f"Task {task.id} Changes", box=box.ROUNDED)
    main_table.add_column("Field", style="cyan")
    main_table.add_column("Original", style="yellow")
    main_table.add_column("Updated", style="green")
    
    # Add rows for changed fields
    if task.title != updated_task.title:
        main_table.add_row("Title", task.title, updated_task.title)
    if task.description != updated_task.description:
        # Truncate long descriptions for display
        orig_desc = task.description[:100] + "..." if len(task.description) > 100 else task.description
        updated_desc = updated_task.description[:100] + "..." if len(updated_task.description) > 100 else updated_task.description
        main_table.add_row("Description", orig_desc, updated_desc)
    
    console.print(main_table)
    
    # Show dependent task updates
    if dependent_updates:
        console.print(f"\n[bold]Dependent Tasks ({len(dependent_updates)}):[/bold]")
        
        for original, updated in dependent_updates:
            dep_table = Table(title=f"Dependent Task [cyan]{original.id}[/cyan] Changes", box=box.ROUNDED)
            dep_table.add_column("Field", style="cyan")
            dep_table.add_column("Original", style="yellow")
            dep_table.add_column("Updated", style="green")
            
            if original.title != updated.title:
                dep_table.add_row("Title", original.title, updated.title)
            if original.description != updated.description:
                # Truncate long descriptions for display
                orig_desc = original.description[:100] + "..." if len(original.description) > 100 else original.description
                updated_desc = updated.description[:100] + "..." if len(updated.description) > 100 else updated.description
                dep_table.add_row("Description", orig_desc, updated_desc)
            
            console.print(dep_table)
            console.print("")
    
    # If preview only, exit
    if preview:
        typer.secho("\nPreview mode - no changes applied.", fg=typer.colors.YELLOW)
        return
    
    # Apply the updates automatically
    with create_spinner("Applying updates..."):
        # Update main task
        task_service.update_item(updated_task)
        
        # Update dependent tasks
        for _, updated_dep in dependent_updates:
            task_service.update_item(updated_dep)
    
    typer.secho(
        f"\nSuccessfully updated task {id} and {len(dependent_updates)} dependent tasks.",
        fg=typer.colors.GREEN,
    )


# Export the commands
__all__ = [
    "add_task_with_ai",
    "update_task_with_ai",
    "expand_task_with_ai",
    "analyze_complexity",
    "generate_tasks_from_prompt",
    "update_task_cascade_with_ai",
] 