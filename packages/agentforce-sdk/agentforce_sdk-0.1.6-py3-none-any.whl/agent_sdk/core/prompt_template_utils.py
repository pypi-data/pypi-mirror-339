"""Utility class for handling prompt template operations."""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from openai import OpenAI
from collections import defaultdict

from ..models.prompt_template import PromptTemplate, PromptInput
from ..exceptions import ValidationError, AgentforceApiError
from .deploy_tools.generate_metadata import MetadataGenerator
from ..config import Config

# Configure logging
logger = logging.getLogger(__name__)

class PromptTemplateUtils:
    """Utility class for handling prompt template operations."""
    
    def __init__(self, sf):
        """Initialize PromptTemplateUtils.
        
        Args:
            sf: Salesforce instance for API operations
        """
        self.sf = sf
        self.API_VERSION = Config.API_VERSION

    def generate_prompt_template(self, name: str, description: str, object_names: Optional[List[str]] = None, output_dir: Optional[str] = None, model: Optional[str] = None) -> PromptTemplate:
        """Generate a prompt template using LLM based on description and Salesforce objects.
        
        Args:
            name (str): Name of the prompt template
            description (str): Description of what the prompt template should do
            object_names (List[str], optional): List of Salesforce object names to consider for field mapping
            output_dir (str, optional): Directory to save the generated template. If not provided, template won't be saved.
            model (str, optional): The model to tune the prompt for (e.g., "gpt-4", "gpt-4o", "llama-2"). Affects prompt style.
            
        Returns:
            PromptTemplate: Generated prompt template with field mappings
            
        Raises:
            ValidationError: If required information is missing
            AgentforceApiError: If API calls fail
        """
        logger.info(f"Generating prompt template '{name}' for description: {description}")
        
        if not name or not description:
            raise ValidationError("Both name and description are required")
            
        try:
            # First, use LLM to analyze the description and suggest fields and template structure
            client = OpenAI()

            # Adjust the analysis prompt based on the model
            model_specific_instructions = ""
            if model:
                if model == "gpt-4o":
                    model_specific_instructions = """
Additional requirements for GPT-4o Optimized:
1. Keep prompts concise and focused
2. Use structured field references with clear type hints
3. Include specific context boundaries
4. Optimize for one-shot responses
5. Use explicit instruction markers"""
                elif model == "llama-2":
                    model_specific_instructions = """
Additional requirements for Llama-2:
1. Use step-by-step instruction format
2. Include more explicit examples
3. Use simpler language constructs
4. Add more context and explanations
5. Use numbered lists for instructions"""
                elif model.startswith("gpt-"):
                    model_specific_instructions = """
Additional requirements for GPT models:
1. Use clear separation between context and instructions
2. Include specific format requirements
3. Use explicit system-style instructions
4. Add validation rules where needed"""

            # If no specific objects provided, try to detect relevant ones from description
            if not object_names:
                try:
                    # Get global describe to list all available objects
                    global_describe = self.sf.describe()
                    available_objects = {
                        obj['name']: {
                            'label': obj['label'],
                            'keyPrefix': obj.get('keyPrefix', ''),
                            'fields': []  # Will be populated on demand
                        }
                        for obj in global_describe['sobjects']
                        if obj['queryable'] and obj['createable']  # Only include accessible objects
                    }
                    
                    # Look for object name mentions in the description
                    desc_lower = description.lower()
                    detected_objects = []
                    
                    for obj_name, obj_info in available_objects.items():
                        # Check if object name or label is mentioned
                        if (obj_name.lower() in desc_lower or 
                            obj_info['label'].lower() in desc_lower):
                            detected_objects.append(obj_name)
                    
                    if detected_objects:
                        object_names = detected_objects
                        logger.info(f"Detected Salesforce objects from description: {', '.join(detected_objects)}")
                    
                except Exception as e:
                    logger.warning(f"Failed to get global describe: {str(e)}")

            # Get Salesforce metadata for detected objects
            sf_field_mappings = {}
            if object_names:
                for obj_name in object_names:
                    try:
                        # Get the SFType object and call describe() on it
                        sf_object = getattr(self.sf, obj_name)
                        obj_desc = sf_object.describe()
                        sf_field_mappings[obj_name] = {
                            field['name'].lower(): {
                                'type': field['type'],
                                'label': field['label'],
                                'description': field.get('inlineHelpText', ''),
                                'nillable': field.get('nillable', True),
                                'picklistValues': field.get('picklistValues', []),
                                'referenceTo': field.get('referenceTo', []),
                                'relationshipName': field.get('relationshipName', '')
                            }
                            for field in obj_desc['fields']
                        }
                    except Exception as e:
                        logger.warning(f"Failed to describe object {obj_name}: {str(e)}")

            # Update the analysis prompt to include Salesforce metadata
            metadata_context = ""
            if sf_field_mappings:
                metadata_context = "\nAvailable Salesforce Objects and Fields:\n"
                for obj_name, fields in sf_field_mappings.items():
                    metadata_context += f"\n{obj_name}:\n"
                    for field_name, field_info in fields.items():
                        metadata_context += f"- {field_name} ({field_info['type']}): {field_info['description'] or field_info['label']}\n"
                        if field_info['referenceTo']:
                            metadata_context += f"  References: {', '.join(field_info['referenceTo'])}\n"

            analysis_prompt = f"""You are an expert in Salesforce development and prompt engineering. Your task is to generate a prompt template based on the following description and available Salesforce metadata. You must respond with ONLY a valid JSON object, no other text.

Description: {description}

{metadata_context}

{model_specific_instructions}

Important Guidelines:
1. Input fields can be:
   a. Primitive types (string, number, boolean, etc.)
   b. Salesforce SObject field references
   c. Apex action outputs for related data queries
2. For Salesforce field references:
   - Use format {{!input.objectName.fieldName}}
   - Example: {{!input.case.subject}}, {{!input.account.name}}
3. For primitive types:
   - Use format {{!input.fieldName}}
   - Example: {{!input.maxResults}}, {{!input.includeHistory}}
4. For Apex action outputs:
   - If you need to query related data (e.g., recent opportunities, open cases), specify an Apex action
   - Use format {{!input.apex.ActionName}} in the template
   - The action will be generated automatically
5. Consider field types when suggesting usage:
   - Use appropriate primitive types for configuration/control fields
   - Use SObject references for direct Salesforce data fields
   - Use Apex actions for related data queries that need filtering/processing
6. Relationship fields should use dot notation:
   - Example: {{!input.case.account.name}} for Case's related Account name

The JSON response must follow this exact structure:
{{
    "inputs": [
        {{
            "name": "field_name",
            "data_type": "string/number/boolean/etc",
            "description": "what this field represents",
            "required": true/false,
            "is_sobject_field": true/false,  # Indicates if this is a Salesforce object field
            "salesforce_mapping": {{  # Only include if is_sobject_field is true
                "object": "ObjectName",
                "field": "FieldName",
                "relationship_field": "RelatedField"  # Optional, for relationship fields
            }},
            "requires_apex_query": false,  # Set to true if this field needs an Apex action
            "apex_action": {{  # Only include if requires_apex_query is true
                "name": "ActionName",  # e.g., GetAccountRecentOpportunities
                "description": "What this action queries",
                "parent_object": "ObjectName",  # e.g., Account
                "query_type": "QueryType"  # e.g., RecentOpportunities
            }}
        }}
    ],
    "prompt_template": "Natural language prompt with field placeholders",
    "instructions": [
        "Specific instruction 1 based on the task",
        "Specific instruction 2 based on the task"
    ]
}}

Remember:
1. Use primitive types for configuration/control parameters
2. Use SObject references for direct Salesforce data fields
3. Suggest Apex actions for complex related data queries
4. Make the prompt_template natural and conversational
5. Include specific, relevant instructions
6. Only output valid JSON, no other text
7. Ensure all JSON keys and values are properly quoted"""

            try:
                response = client.chat.completions.create(
                    model=model if model else "gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a JSON-only response bot. Only output valid JSON objects, no other text."},
                        {"role": "user", "content": analysis_prompt}
                    ],
                    temperature=0.2
                )
                
                # Get the response content and clean it
                content = response.choices[0].message.content.strip()
                
                # If the response is wrapped in ```json or ``` markers, remove them
                if content.startswith("```"):
                    content = content.split("```")[1]
                    if content.startswith("json"):
                        content = content[4:]
                content = content.strip()
                
                # Parse the cleaned JSON
                try:
                    llm_analysis = json.loads(content)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse cleaned LLM response: {content}")
                    logger.error(f"JSON parse error: {str(e)}")
                    raise AgentforceApiError(f"Failed to generate valid prompt template: {str(e)}")
                
                # Validate the required fields are present
                required_fields = ["inputs", "prompt_template", "instructions"]
                missing_fields = [field for field in required_fields if field not in llm_analysis]
                if missing_fields:
                    raise AgentforceApiError(f"LLM response missing required fields: {', '.join(missing_fields)}")
                
            except Exception as e:
                logger.error(f"OpenAI API call failed: {str(e)}")
                raise AgentforceApiError(f"Failed to generate prompt template: {str(e)}")
            
            # Convert LLM suggested inputs to Input model instances and handle Apex actions
            input_fields = []
            apex_actions = []
            
            # Process each input field from LLM analysis
            for field in llm_analysis["inputs"]:
                field_data = {
                    "name": field["name"],
                    "data_type": field["data_type"],
                    "description": field["description"],
                    "is_required": field["required"]
                }

                if field.get("requires_apex_query") and (apex_info := field.get("apex_action")):
                    # Store Apex action info for later generation
                    apex_actions.append({
                        "name": apex_info["name"],
                        "description": apex_info["description"],
                        "parent_object": apex_info["parent_object"],
                        "query_type": apex_info["query_type"]
                    })
                    
                    # Add Apex reference field
                    field_data.update({
                        "data_type": "apex",
                        "salesforce_field": apex_info["name"],
                        "salesforce_object": "apex"
                    })
                elif field.get("is_sobject_field") and (sf_mapping := field.get("salesforce_mapping")):
                    # Add Salesforce field mapping
                    field_data.update({
                        "salesforce_field": sf_mapping.get("field"),
                        "salesforce_object": sf_mapping.get("object")
                    })

                input_fields.append(PromptInput(**field_data))

            # Group and process fields for template
            grouped_fields = defaultdict(list)
            for field in input_fields:
                group = 'primitive' if not field.salesforce_object else field.salesforce_object
                grouped_fields[group].append(field)

            # Process template text and create final fields list
            template_text = llm_analysis["prompt_template"]
            final_fields = []

            for object_name, fields in grouped_fields.items():
                if object_name == 'primitive':
                    final_fields.extend(fields)
                else:
                    # Add object reference field for non-primitive types
                    if object_name != 'apex':
                        field = fields[0]
                        final_fields.append(PromptInput(
                            name=field.salesforce_object.lower(),
                            data_type=field.salesforce_object,
                            description=field.description,
                            is_required=field.is_required
                        ))
                    # Update template placeholders
                    for field in fields:
                        if object_name != 'primitive':
                            template_text = template_text.replace(
                                f"{{!input.{field.name}}}", 
                                f"{{!$Input:{field.salesforce_object.lower()}.{field.salesforce_field}}}"
                            )
                        else:
                            template_text = template_text.replace(
                                f"{{!input.{field.name}}}", 
                                f"{{!$Input:{field.name}}}"
                            )

            # Generate Apex classes if needed
            if output_dir:
                apex_dir = os.path.join(output_dir or os.getcwd(), "apex")
                os.makedirs(apex_dir, exist_ok=True)
                
                # Generate data query Apex classes
                for action in apex_actions:
                    apex_code = self._generate_apex_action(
                        class_name=action["name"],
                        parent_object=action["parent_object"],
                        query_type=action["query_type"],
                        description=action["description"],
                        input_fields=final_fields
                    )
                    with open(os.path.join(apex_dir, f"{action['name']}.cls"), "w") as f:
                        f.write(apex_code)
                    logger.info(f"Generated Apex action: {action['name']}")
                    template_text = template_text + "\n\n" +action["description"] + ":\n" f"{{!$Apex:.{action['name']}}}\n"                     

                # Generate prompt template Apex class
                template_class_name = f"{name.replace(' ', '')}Template"
                prompt_apex_code = self._generate_apex_action(
                    class_name=template_class_name,
                    parent_object="",  # Not needed for prompt template
                    query_type="prompt",
                    description=description,
                    input_fields=final_fields
                )
                with open(os.path.join(apex_dir, f"{template_class_name}.cls"), "w") as f:
                    f.write(prompt_apex_code)
                logger.info(f"Generated prompt template Apex class: {template_class_name}")

            # Create final template
            template = PromptTemplate(
                name=name,
                description=description,
                input_fields=final_fields,
                output_fields=[],
                template_text=template_text
            )
            
            # Save the template if output directory is provided
            if output_dir:
                self.save_prompt_template(template, output_dir)
            
            logger.info(f"Successfully generated prompt template: {name}")
            return template
            
        except Exception as e:
            logger.error(f"Failed to generate prompt template '{name}': {str(e)}")
            raise AgentforceApiError(f"Failed to generate prompt template: {str(e)}")

    def _generate_apex_action(self, class_name: str, parent_object: str, query_type: str, description: str, input_fields: Optional[List[PromptInput]] = None) -> str:
        """Generate an Apex invocable action for querying related data or prompt templates.
        
        Args:
            class_name (str): Name of the Apex class
            parent_object (str): Parent Salesforce object (e.g., Account)
            query_type (str): Type of query (e.g., RecentOpportunities) or 'prompt' for templates
            description (str): Description of what the action does
            input_fields (List[PromptInput], optional): List of input fields for prompt templates
            
        Returns:
            str: Generated Apex code
        """
        # Call OpenAI to generate the Apex class
        client = OpenAI()

        if query_type == 'prompt' and input_fields:
            # Generate prompt template Apex class
            prompt = f"""Generate an Apex Invocable Action class with the following specifications:

Class Name: {class_name}
Description: {description}

Requirements:
1. Create an Invocable Action that takes input fields as Request class parameters
2. Return a Response class with ONLY a single Prompt field
3. Follow the exact format shown in the example below
4. Include proper error handling
5. Include appropriate comments and documentation
6. Use JSON.serialize() for any complex data structures

Input Fields:
{json.dumps([{
    "name": field.name,
    "object": field.salesforce_object,
    "field": field.salesforce_field,
    "required": field.is_required
} for field in input_fields], indent=2)}

Example Format:
public class {class_name} {{
    @InvocableMethod
    public static List<Response> getPrompt(List<Request> requests) {{
        Request input = requests[0];
        List<Response> responses = new List<Response>();
        Response output = new Response();
        
        try {{
            // Create a map to hold the field values
            Map<String, Object> promptData = new Map<String, Object>();
            
            // Add field values to the map
            // Example: promptData.put('accountName', input.Account.Name);
            
            // Convert the map to a JSON string
            output.Prompt = JSON.serialize(promptData);
        }} catch(Exception e) {{
            output.Prompt = JSON.serialize(new Map<String, Object>{{
                'error' => e.getMessage(),
                'stackTrace' => e.getStackTraceString()
            }});
        }}
        
        responses.add(output);
        return responses;
    }}
    
    public class Request {{
        // Input fields here with @InvocableVariable
    }}
    
    public class Response {{
        @InvocableVariable(required=true)
        public String Prompt;
    }}
}}

IMPORTANT: 
1. The Response class MUST be exactly as shown above, with only a single Prompt field
2. All outputs MUST be JSON serialized strings
3. Include proper error handling with JSON formatted error responses

Please provide the complete Apex class implementation following this exact structure."""
        else:
            # Generate data query Apex class
            prompt = f"""Generate an Apex Invocable Action class with the following specifications:

Class Name: {class_name}
Description: {description}
Parent Object: {parent_object}
Query Type: {query_type}

Requirements:
1. Create an Invocable Action that takes a {parent_object} Id as input
2. Query for {query_type} related to the {parent_object}
3. Include proper error handling and limits checking
4. Return a Response class with ONLY a single Prompt field containing the JSON serialized query results
5. Follow Salesforce best practices
6. Use JSON.serialize() for the output

The class must follow this exact structure:
public class {class_name} {{
    @InvocableMethod
    public static List<Response> execute(List<Request> requests) {{
        Request input = requests[0];
        Response output = new Response();
        
        try {{
            // Query the data
            List<SObject> results = [/* Your SOQL query here */];
            
            // Convert results to a map/list structure
            List<Map<String, Object>> formattedResults = new List<Map<String, Object>>();
            for(SObject record : results) {{
                formattedResults.add(record.getPopulatedFieldsAsMap());
            }}
            
            // Serialize the results to JSON
            output.Prompt = JSON.serialize(formattedResults);
            
        }} catch(Exception e) {{
            output.Prompt = JSON.serialize(new Map<String, Object>{{
                'error' => e.getMessage(),
                'stackTrace' => e.getStackTraceString()
            }});
        }}
        
        return new List<Response>>{{ output }};
    }}
    
    public class Request {{
        @InvocableVariable(required=true)
        public Id recordId;
    }}
    
    public class Response {{
        @InvocableVariable(required=true)
        public String Prompt;
    }}
}}

IMPORTANT: 
1. The Response class MUST be exactly as shown above, with only a single Prompt field
2. All outputs MUST be JSON serialized strings
3. Include proper error handling with JSON formatted error responses

Please provide the complete Apex class implementation following this exact structure."""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert Salesforce developer specializing in Apex invocable actions. Always ensure Response class has only a Prompt field and all outputs are JSON serialized."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        
        apex_code = response.choices[0].message.content
        
        # Clean up the code
        if "```apex" in apex_code:
            apex_code = apex_code.split("```apex")[1].split("```")[0].strip()
        elif "```java" in apex_code:
            apex_code = apex_code.split("```java")[1].split("```")[0].strip()
        elif "```" in apex_code:
            apex_code = apex_code.split("```")[1].split("```")[0].strip()
        
        return apex_code

    def save_prompt_template(self, template: PromptTemplate, output_dir: str) -> str:
        """Save a prompt template to the specified output directory.
        
        Args:
            template (PromptTemplate): The prompt template to save
            output_dir (str): Directory to save the template
            
        Returns:
            str: Path to the saved template file
            
        Raises:
            ValidationError: If required information is missing
            AgentforceApiError: If saving fails
        """
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Create a sanitized filename from the template name
            template_name = MetadataGenerator._sanitize_name(template.name).lower()
            template_file = os.path.join(output_dir, f"{template_name}.json")
            
            # Convert template to dictionary format
            template_data = template.to_dict()
            
            # Save the template
            with open(template_file, 'w') as f:
                json.dump(template_data, f, indent=2)
                
            logger.info(f"Successfully saved prompt template to: {template_file}")
            return template_file
            
        except Exception as e:
            logger.error(f"Failed to save prompt template: {str(e)}")
            raise AgentforceApiError(f"Failed to save prompt template: {str(e)}")

    def load_template(self, template_path: str) -> PromptTemplate:
        """Load a prompt template from a JSON file.
        
        Args:
            template_path (str): Path to the template JSON file
            
        Returns:
            PromptTemplate: Loaded prompt template
            
        Raises:
            ValidationError: If the file doesn't exist or has invalid format
            AgentforceApiError: If loading fails
        """
        try:
            if not os.path.exists(template_path):
                raise ValidationError(f"Template file not found: {template_path}")
                
            with open(template_path, 'r') as f:
                template_data = json.load(f)
                
            return PromptTemplate.from_dict(template_data)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse template file: {str(e)}")
            raise ValidationError(f"Invalid template format in {template_path}: {str(e)}")
        except Exception as e:
            logger.error(f"Failed to load template: {str(e)}")
            raise AgentforceApiError(f"Failed to load template: {str(e)}")

    def tune_prompt_template(self, template_path: str, description: str, model: str, output_dir: Optional[str] = None) -> PromptTemplate:
        """Tune an existing prompt template for a specific model and enhance it based on description.
        
        Args:
            template_path (str): Path to the existing template JSON file
            description (str): Additional description or context for tuning
            model (str): The model to tune the template for (e.g., "gpt-4", "gpt-4o", "llama-2")
            output_dir (str, optional): Directory to save the tuned template. If not provided, won't save.
            
        Returns:
            PromptTemplate: Tuned prompt template with enhanced fields and instructions
            
        Raises:
            ValidationError: If required information is missing
            AgentforceApiError: If API calls fail
        """
        logger.info(f"Tuning prompt template from {template_path} for model: {model}")
        
        try:
            # Load the existing template
            with open(template_path, 'r') as f:
                existing_template = json.load(f)
            
            # Convert to PromptTemplate instance
            current_template = PromptTemplate.from_dict(existing_template)
            
            # Create enhanced description combining original and new context
            enhanced_description = f"""Original Template Description: {current_template.description}
Additional Context/Requirements: {description}

Current Template Structure:
{current_template.template_text}

Please enhance this template by:
1. Maintaining compatibility with existing fields
2. Suggesting additional fields that would improve the template
3. Optimizing the prompt text for the specified model ({model})
4. Enhancing instructions for better results"""

            # Generate enhanced template using the existing method
            enhanced_template = self.generate_prompt_template(
                name=f"{current_template.name}_enhanced_{model}",
                description=enhanced_description,
                object_names=[field.salesforce_object for field in current_template.input_fields if field.salesforce_object],
                output_dir=output_dir,
                model=model
            )
            
            logger.info(f"Successfully enhanced template for {model}")
            return enhanced_template
            
        except Exception as e:
            logger.error(f"Failed to tune prompt template: {str(e)}")
            raise AgentforceApiError(f"Failed to tune prompt template: {str(e)}") 