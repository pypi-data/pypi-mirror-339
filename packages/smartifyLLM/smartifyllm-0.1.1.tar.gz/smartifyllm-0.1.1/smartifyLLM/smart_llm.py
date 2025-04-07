from typing import Dict, Union, Tuple, List, Optional

#custom imports
from .web_tools import *
from .prompts import DEFAULT_PROMPT
from .advanced_finance import *

class Smartify:
    def __init__(self, model_pipeline):
        self.model_pipeline = model_pipeline
    
    def smart_response(self, query: str, custom_prompt: str = None, 
                                    custom_context: Optional[Dict[str, str]] = None,
                                    max_context_tokens: int = 4000,
                                    buffer: int = 200,
                                    return_source: bool = False,
                                    advanced_stockmrkt = False
        ) -> Union[str, Tuple[str, List[str]]]:
        
        """
        Generates a smart response using custom or online context.

        Args:
            query (str): The input question.
            custom_prompt (str, optional): A custom prompt format.
            custom_context (Dict[str, str], optional): Predefined sources for context.
            max_context_tokens (int, optional): Max tokens for context (default: 4000).
            buffer (int, optional): Token buffer to prevent overflow (default: 200).
            return_source (bool, optional): If True, returns sources with response.
            advanced_stockmrkt: If True, checks stock market data to get the share price of company (default: False).

        Returns:
            str | Tuple[str, List[str]]: The response, with sources if `return_source=True`.
        """

        if advanced_stockmrkt:
            stock_data = find_stock_price(query)
            if stock_data: 
                price = stock_data[0]["price"]
                response = (f"The current price of {stock_data[0]['name']} stock "
                        f"({stock_data[0]['symbol']}) is ${price:.2f} "
                        f"(Source: Yahoo Finance).")
                return (response, ["Yahoo Finance"]) if return_source else response

        if custom_context is not None:
            best_source, best_content = rank_best_answer(query, custom_context)
            sources = [best_source] if best_source else []
        else:
            web_context = get_online_results(query=query, num_results=3)
            best_source, best_content = rank_best_answer(query, web_context)
            sources = [best_source] if best_source else []
        
        if not best_content:
            response = self.model_pipeline(query)
            return (response, []) if return_source else response
        
        template = custom_prompt or DEFAULT_PROMPT
        max_content_tokens = max_context_tokens - buffer - len(template.split()) - len(query.split())
        
        truncated_content = " ".join(best_content.split()[:max_content_tokens])
        
        try:
            response = self.model_pipeline(template.format(context=truncated_content, query=query))
        except TypeError:
            response = self.model_pipeline(template.format(context=truncated_content, query=query))

        return (response, sources) if return_source else response
