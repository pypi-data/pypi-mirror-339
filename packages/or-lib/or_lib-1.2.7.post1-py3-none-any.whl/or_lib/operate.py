# from __future__ import annotations

# import asyncio
# import json
# import re
# import os
# from typing import Any, AsyncIterator
# from collections import Counter, defaultdict

# from .utils import (
#     logger,
#     clean_str,
#     compute_mdhash_id,
#     decode_tokens_by_tiktoken,
#     encode_string_by_tiktoken,
#     is_float_regex,
#     list_of_list_to_csv,
#     pack_user_ass_to_openai_messages,
#     split_string_by_multi_markers,
#     truncate_list_by_token_size,
#     process_combine_contexts,
#     compute_args_hash,
#     handle_cache,
#     save_to_cache,
#     CacheData,
#     statistic_data,
#     get_conversation_turns,
#     verbose_debug,
# )
# from .base import (
#     BaseGraphStorage,
#     BaseKVStorage,
#     BaseVectorStorage,
#     TextChunkSchema,
#     QueryParam,
# )
# from .prompt import GRAPH_FIELD_SEP, PROMPTS
# import time
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv(override=True)


# def chunking_by_token_size(
#     content: str,
#     split_by_character: str | None = None,
#     split_by_character_only: bool = False,
#     overlap_token_size: int = 128,
#     max_token_size: int = 1024,
#     tiktoken_model: str = "gpt-4o",
# ) -> list[dict[str, Any]]:
#     tokens = encode_string_by_tiktoken(content, model_name=tiktoken_model)
#     results: list[dict[str, Any]] = []
#     if split_by_character:
#         raw_chunks = content.split(split_by_character)
#         new_chunks = []
#         if split_by_character_only:
#             for chunk in raw_chunks:
#                 _tokens = encode_string_by_tiktoken(chunk, model_name=tiktoken_model)
#                 new_chunks.append((len(_tokens), chunk))
#         else:
#             for chunk in raw_chunks:
#                 _tokens = encode_string_by_tiktoken(chunk, model_name=tiktoken_model)
#                 if len(_tokens) > max_token_size:
#                     for start in range(
#                         0, len(_tokens), max_token_size - overlap_token_size
#                     ):
#                         chunk_content = decode_tokens_by_tiktoken(
#                             _tokens[start : start + max_token_size],
#                             model_name=tiktoken_model,
#                         )
#                         new_chunks.append(
#                             (min(max_token_size, len(_tokens) - start), chunk_content)
#                         )
#                 else:
#                     new_chunks.append((len(_tokens), chunk))
#         for index, (_len, chunk) in enumerate(new_chunks):
#             results.append(
#                 {
#                     "tokens": _len,
#                     "content": chunk.strip(),
#                     "chunk_order_index": index,
#                 }
#             )
#     else:
#         for index, start in enumerate(
#             range(0, len(tokens), max_token_size - overlap_token_size)
#         ):
#             chunk_content = decode_tokens_by_tiktoken(
#                 tokens[start : start + max_token_size], model_name=tiktoken_model
#             )
#             results.append(
#                 {
#                     "tokens": min(max_token_size, len(tokens) - start),
#                     "content": chunk_content.strip(),
#                     "chunk_order_index": index,
#                 }
#             )
#     return results


# async def _handle_entity_relation_summary(
#     entity_or_relation_name: str,
#     description: str,
#     global_config: dict,
# ) -> str:
#     """Handle entity relation summary
#     For each entity or relation, input is the combined description of already existing description and new description.
#     If too long, use LLM to summarize.
#     """
#     use_llm_func: callable = global_config["llm_model_func"]
#     llm_max_tokens = global_config["llm_model_max_token_size"]
#     tiktoken_model_name = global_config["tiktoken_model_name"]
#     summary_max_tokens = global_config["entity_summary_to_max_tokens"]
#     language = global_config["addon_params"].get(
#         "language", PROMPTS["DEFAULT_LANGUAGE"]
#     )

#     tokens = encode_string_by_tiktoken(description, model_name=tiktoken_model_name)
#     if len(tokens) < summary_max_tokens:  # No need for summary
#         return description
#     prompt_template = PROMPTS["summarize_entity_descriptions"]
#     use_description = decode_tokens_by_tiktoken(
#         tokens[:llm_max_tokens], model_name=tiktoken_model_name
#     )
#     context_base = dict(
#         entity_name=entity_or_relation_name,
#         description_list=use_description.split(GRAPH_FIELD_SEP),
#         language=language,
#     )
#     use_prompt = prompt_template.format(**context_base)
#     logger.debug(f"Trigger summary: {entity_or_relation_name}")
#     summary = await use_llm_func(use_prompt, max_tokens=summary_max_tokens)
#     return summary


# async def _handle_single_entity_extraction(
#     record_attributes: list[str],
#     chunk_key: str,
#     file_path: str = "unknown_source",
# ):
#     if len(record_attributes) < 4 or record_attributes[0] != '"entity"':
#         return None

#     # Clean and validate entity name
#     entity_name = clean_str(record_attributes[1]).strip('"')
#     if not entity_name.strip():
#         logger.warning(
#             f"Entity extraction error: empty entity name in: {record_attributes}"
#         )
#         return None

#     # Clean and validate entity type
#     entity_type = clean_str(record_attributes[2]).strip('"')
#     if not entity_type.strip() or entity_type.startswith('("'):
#         logger.warning(
#             f"Entity extraction error: invalid entity type in: {record_attributes}"
#         )
#         return None

#     # Clean and validate description
#     entity_description = clean_str(record_attributes[3]).strip('"')
#     if not entity_description.strip():
#         logger.warning(
#             f"Entity extraction error: empty description for entity '{entity_name}' of type '{entity_type}'"
#         )
#         return None

#     return dict(
#         entity_name=entity_name,
#         entity_type=entity_type,
#         description=entity_description,
#         source_id=chunk_key,
#         file_path=file_path,
#     )


# async def _handle_single_relationship_extraction(
#     record_attributes: list[str],
#     chunk_key: str,
#     file_path: str = "unknown_source",
# ):
#     if len(record_attributes) < 5 or record_attributes[0] != '"relationship"':
#         return None
#     # add this record as edge
#     source = clean_str(record_attributes[1]).strip('"')
#     target = clean_str(record_attributes[2]).strip('"')
#     edge_description = clean_str(record_attributes[3]).strip('"')
#     edge_keywords = clean_str(record_attributes[4]).strip('"')
#     edge_source_id = chunk_key
#     weight = (
#         float(record_attributes[-1].strip('"'))
#         if is_float_regex(record_attributes[-1])
#         else 1.0
#     )
#     return dict(
#         src_id=source,
#         tgt_id=target,
#         weight=weight,
#         description=edge_description,
#         keywords=edge_keywords,
#         source_id=edge_source_id,
#         file_path=file_path,
#     )


# async def _merge_nodes_then_upsert(
#     entity_name: str,
#     nodes_data: list[dict],
#     knowledge_graph_inst: BaseGraphStorage,
#     global_config: dict,
# ):
#     """Get existing nodes from knowledge graph use name,if exists, merge data, else create, then upsert."""
#     already_entity_types = []
#     already_source_ids = []
#     already_description = []
#     already_file_paths = []

#     already_node = await knowledge_graph_inst.get_node(entity_name)
#     if already_node is not None:
#         already_entity_types.append(already_node["entity_type"])
#         already_source_ids.extend(
#             split_string_by_multi_markers(already_node["source_id"], [GRAPH_FIELD_SEP])
#         )
#         already_file_paths.extend(
#             split_string_by_multi_markers(already_node["file_path"], [GRAPH_FIELD_SEP])
#         )
#         already_description.append(already_node["description"])

#     entity_type = sorted(
#         Counter(
#             [dp["entity_type"] for dp in nodes_data] + already_entity_types
#         ).items(),
#         key=lambda x: x[1],
#         reverse=True,
#     )[0][0]
#     description = GRAPH_FIELD_SEP.join(
#         sorted(set([dp["description"] for dp in nodes_data] + already_description))
#     )
#     source_id = GRAPH_FIELD_SEP.join(
#         set([dp["source_id"] for dp in nodes_data] + already_source_ids)
#     )
#     file_path = GRAPH_FIELD_SEP.join(
#         set([dp["file_path"] for dp in nodes_data] + already_file_paths)
#     )

#     logger.debug(f"file_path: {file_path}")
#     description = await _handle_entity_relation_summary(
#         entity_name, description, global_config
#     )
#     node_data = dict(
#         entity_id=entity_name,
#         entity_type=entity_type,
#         description=description,
#         source_id=source_id,
#         file_path=file_path,
#     )
#     await knowledge_graph_inst.upsert_node(
#         entity_name,
#         node_data=node_data,
#     )
#     node_data["entity_name"] = entity_name
#     return node_data


# async def _merge_edges_then_upsert(
#     src_id: str,
#     tgt_id: str,
#     edges_data: list[dict],
#     knowledge_graph_inst: BaseGraphStorage,
#     global_config: dict,
# ):
#     already_weights = []
#     already_source_ids = []
#     already_description = []
#     already_keywords = []
#     already_file_paths = []

#     if await knowledge_graph_inst.has_edge(src_id, tgt_id):
#         already_edge = await knowledge_graph_inst.get_edge(src_id, tgt_id)
#         # Handle the case where get_edge returns None or missing fields
#         if already_edge:
#             # Get weight with default 0.0 if missing
#             already_weights.append(already_edge.get("weight", 0.0))

#             # Get source_id with empty string default if missing or None
#             if already_edge.get("source_id") is not None:
#                 already_source_ids.extend(
#                     split_string_by_multi_markers(
#                         already_edge["source_id"], [GRAPH_FIELD_SEP]
#                     )
#                 )

#             # Get file_path with empty string default if missing or None
#             if already_edge.get("file_path") is not None:
#                 already_file_paths.extend(
#                     split_string_by_multi_markers(
#                         already_edge["file_path"], [GRAPH_FIELD_SEP]
#                     )
#                 )

#             # Get description with empty string default if missing or None
#             if already_edge.get("description") is not None:
#                 already_description.append(already_edge["description"])

#             # Get keywords with empty string default if missing or None
#             if already_edge.get("keywords") is not None:
#                 already_keywords.extend(
#                     split_string_by_multi_markers(
#                         already_edge["keywords"], [GRAPH_FIELD_SEP]
#                     )
#                 )

#     # Process edges_data with None checks
#     weight = sum([dp["weight"] for dp in edges_data] + already_weights)
#     description = GRAPH_FIELD_SEP.join(
#         sorted(
#             set(
#                 [dp["description"] for dp in edges_data if dp.get("description")]
#                 + already_description
#             )
#         )
#     )
#     keywords = GRAPH_FIELD_SEP.join(
#         sorted(
#             set(
#                 [dp["keywords"] for dp in edges_data if dp.get("keywords")]
#                 + already_keywords
#             )
#         )
#     )
#     source_id = GRAPH_FIELD_SEP.join(
#         set(
#             [dp["source_id"] for dp in edges_data if dp.get("source_id")]
#             + already_source_ids
#         )
#     )
#     file_path = GRAPH_FIELD_SEP.join(
#         set(
#             [dp["file_path"] for dp in edges_data if dp.get("file_path")]
#             + already_file_paths
#         )
#     )

#     for need_insert_id in [src_id, tgt_id]:
#         if not (await knowledge_graph_inst.has_node(need_insert_id)):
#             await knowledge_graph_inst.upsert_node(
#                 need_insert_id,
#                 node_data={
#                     "entity_id": need_insert_id,
#                     "source_id": source_id,
#                     "description": description,
#                     "entity_type": "UNKNOWN",
#                     "file_path": file_path,
#                 },
#             )
#     description = await _handle_entity_relation_summary(
#         f"({src_id}, {tgt_id})", description, global_config
#     )
#     await knowledge_graph_inst.upsert_edge(
#         src_id,
#         tgt_id,
#         edge_data=dict(
#             weight=weight,
#             description=description,
#             keywords=keywords,
#             source_id=source_id,
#             file_path=file_path,
#         ),
#     )

#     edge_data = dict(
#         src_id=src_id,
#         tgt_id=tgt_id,
#         description=description,
#         keywords=keywords,
#         source_id=source_id,
#         file_path=file_path,
#     )

#     return edge_data


# async def extract_entities(
#     chunks: dict[str, TextChunkSchema],
#     knowledge_graph_inst: BaseGraphStorage,
#     entity_vdb: BaseVectorStorage,
#     relationships_vdb: BaseVectorStorage,
#     global_config: dict[str, str],
#     pipeline_status: dict = None,
#     pipeline_status_lock=None,
#     llm_response_cache: BaseKVStorage | None = None,
# ) -> None:
#     use_llm_func: callable = global_config["llm_model_func"]
#     entity_extract_max_gleaning = global_config["entity_extract_max_gleaning"]
#     enable_llm_cache_for_entity_extract: bool = global_config[
#         "enable_llm_cache_for_entity_extract"
#     ]

#     ordered_chunks = list(chunks.items())
#     # add language and example number params to prompt
#     language = global_config["addon_params"].get(
#         "language", PROMPTS["DEFAULT_LANGUAGE"]
#     )
#     entity_types = global_config["addon_params"].get(
#         "entity_types", PROMPTS["DEFAULT_ENTITY_TYPES"]
#     )
#     example_number = global_config["addon_params"].get("example_number", None)
#     if example_number and example_number < len(PROMPTS["entity_extraction_examples"]):
#         examples = "\n".join(
#             PROMPTS["entity_extraction_examples"][: int(example_number)]
#         )
#     else:
#         examples = "\n".join(PROMPTS["entity_extraction_examples"])

#     example_context_base = dict(
#         tuple_delimiter=PROMPTS["DEFAULT_TUPLE_DELIMITER"],
#         record_delimiter=PROMPTS["DEFAULT_RECORD_DELIMITER"],
#         completion_delimiter=PROMPTS["DEFAULT_COMPLETION_DELIMITER"],
#         entity_types=", ".join(entity_types),
#         language=language,
#     )
#     # add example's format
#     examples = examples.format(**example_context_base)

#     entity_extract_prompt = PROMPTS["entity_extraction"]
#     context_base = dict(
#         tuple_delimiter=PROMPTS["DEFAULT_TUPLE_DELIMITER"],
#         record_delimiter=PROMPTS["DEFAULT_RECORD_DELIMITER"],
#         completion_delimiter=PROMPTS["DEFAULT_COMPLETION_DELIMITER"],
#         entity_types=",".join(entity_types),
#         examples=examples,
#         language=language,
#     )

#     continue_prompt = PROMPTS["entity_continue_extraction"].format(**context_base)
#     if_loop_prompt = PROMPTS["entity_if_loop_extraction"]

#     processed_chunks = 0
#     total_chunks = len(ordered_chunks)

#     async def _user_llm_func_with_cache(
#         input_text: str, history_messages: list[dict[str, str]] = None
#     ) -> str:
#         if enable_llm_cache_for_entity_extract and llm_response_cache:
#             if history_messages:
#                 history = json.dumps(history_messages, ensure_ascii=False)
#                 _prompt = history + "\n" + input_text
#             else:
#                 _prompt = input_text

#             # TODO： add cache_type="extract"
#             arg_hash = compute_args_hash(_prompt)
#             cached_return, _1, _2, _3 = await handle_cache(
#                 llm_response_cache,
#                 arg_hash,
#                 _prompt,
#                 "default",
#                 cache_type="extract",
#             )
#             if cached_return:
#                 logger.debug(f"Found cache for {arg_hash}")
#                 statistic_data["llm_cache"] += 1
#                 return cached_return
#             statistic_data["llm_call"] += 1
#             if history_messages:
#                 res: str = await use_llm_func(
#                     input_text, history_messages=history_messages
#                 )
#             else:
#                 res: str = await use_llm_func(input_text)
#             await save_to_cache(
#                 llm_response_cache,
#                 CacheData(
#                     args_hash=arg_hash,
#                     content=res,
#                     prompt=_prompt,
#                     cache_type="extract",
#                 ),
#             )
#             return res

#         if history_messages:
#             return await use_llm_func(input_text, history_messages=history_messages)
#         else:
#             return await use_llm_func(input_text)

#     async def _process_extraction_result(
#         result: str, chunk_key: str, file_path: str = "unknown_source"
#     ):
#         """Process a single extraction result (either initial or gleaning)
#         Args:
#             result (str): The extraction result to process
#             chunk_key (str): The chunk key for source tracking
#             file_path (str): The file path for citation
#         Returns:
#             tuple: (nodes_dict, edges_dict) containing the extracted entities and relationships
#         """
#         maybe_nodes = defaultdict(list)
#         maybe_edges = defaultdict(list)

#         records = split_string_by_multi_markers(
#             result,
#             [context_base["record_delimiter"], context_base["completion_delimiter"]],
#         )

#         for record in records:
#             record = re.search(r"\((.*)\)", record)
#             if record is None:
#                 continue
#             record = record.group(1)
#             record_attributes = split_string_by_multi_markers(
#                 record, [context_base["tuple_delimiter"]]
#             )

#             if_entities = await _handle_single_entity_extraction(
#                 record_attributes, chunk_key, file_path
#             )
#             if if_entities is not None:
#                 maybe_nodes[if_entities["entity_name"]].append(if_entities)
#                 continue

#             if_relation = await _handle_single_relationship_extraction(
#                 record_attributes, chunk_key, file_path
#             )
#             if if_relation is not None:
#                 maybe_edges[(if_relation["src_id"], if_relation["tgt_id"])].append(
#                     if_relation
#                 )

#         return maybe_nodes, maybe_edges

#     async def _process_single_content(chunk_key_dp: tuple[str, TextChunkSchema]):
#         """Process a single chunk
#         Args:
#             chunk_key_dp (tuple[str, TextChunkSchema]):
#                 ("chunk-xxxxxx", {"tokens": int, "content": str, "full_doc_id": str, "chunk_order_index": int})
#         """
#         nonlocal processed_chunks
#         chunk_key = chunk_key_dp[0]
#         chunk_dp = chunk_key_dp[1]
#         content = chunk_dp["content"]
#         # Get file path from chunk data or use default
#         file_path = chunk_dp.get("file_path", "unknown_source")

#         # Get initial extraction
#         hint_prompt = entity_extract_prompt.format(
#             **context_base, input_text="{input_text}"
#         ).format(**context_base, input_text=content)

#         final_result = await _user_llm_func_with_cache(hint_prompt)
#         history = pack_user_ass_to_openai_messages(hint_prompt, final_result)

#         # Process initial extraction with file path
#         maybe_nodes, maybe_edges = await _process_extraction_result(
#             final_result, chunk_key, file_path
#         )

#         # Process additional gleaning results
#         for now_glean_index in range(entity_extract_max_gleaning):
#             glean_result = await _user_llm_func_with_cache(
#                 continue_prompt, history_messages=history
#             )

#             history += pack_user_ass_to_openai_messages(continue_prompt, glean_result)

#             # Process gleaning result separately with file path
#             glean_nodes, glean_edges = await _process_extraction_result(
#                 glean_result, chunk_key, file_path
#             )

#             # Merge results
#             for entity_name, entities in glean_nodes.items():
#                 maybe_nodes[entity_name].extend(entities)
#             for edge_key, edges in glean_edges.items():
#                 maybe_edges[edge_key].extend(edges)

#             if now_glean_index == entity_extract_max_gleaning - 1:
#                 break

#             if_loop_result: str = await _user_llm_func_with_cache(
#                 if_loop_prompt, history_messages=history
#             )
#             if_loop_result = if_loop_result.strip().strip('"').strip("'").lower()
#             if if_loop_result != "yes":
#                 break

#         processed_chunks += 1
#         entities_count = len(maybe_nodes)
#         relations_count = len(maybe_edges)
#         log_message = f"  Chunk {processed_chunks}/{total_chunks}: extracted {entities_count} entities and {relations_count} relationships (deduplicated)"
#         logger.info(log_message)
#         if pipeline_status is not None:
#             async with pipeline_status_lock:
#                 pipeline_status["latest_message"] = log_message
#                 pipeline_status["history_messages"].append(log_message)
#         return dict(maybe_nodes), dict(maybe_edges)

#     tasks = [_process_single_content(c) for c in ordered_chunks]
#     results = await asyncio.gather(*tasks)

#     maybe_nodes = defaultdict(list)
#     maybe_edges = defaultdict(list)
#     for m_nodes, m_edges in results:
#         for k, v in m_nodes.items():
#             maybe_nodes[k].extend(v)
#         for k, v in m_edges.items():
#             maybe_edges[tuple(sorted(k))].extend(v)

#     from .kg.shared_storage import get_graph_db_lock

#     graph_db_lock = get_graph_db_lock(enable_logging=False)

#     # Ensure that nodes and edges are merged and upserted atomically
#     async with graph_db_lock:
#         all_entities_data = await asyncio.gather(
#             *[
#                 _merge_nodes_then_upsert(k, v, knowledge_graph_inst, global_config)
#                 for k, v in maybe_nodes.items()
#             ]
#         )

#         all_relationships_data = await asyncio.gather(
#             *[
#                 _merge_edges_then_upsert(
#                     k[0], k[1], v, knowledge_graph_inst, global_config
#                 )
#                 for k, v in maybe_edges.items()
#             ]
#         )

#     if not (all_entities_data or all_relationships_data):
#         log_message = "Didn't extract any entities and relationships."
#         logger.info(log_message)
#         if pipeline_status is not None:
#             async with pipeline_status_lock:
#                 pipeline_status["latest_message"] = log_message
#                 pipeline_status["history_messages"].append(log_message)
#         return

#     if not all_entities_data:
#         log_message = "Didn't extract any entities"
#         logger.info(log_message)
#         if pipeline_status is not None:
#             async with pipeline_status_lock:
#                 pipeline_status["latest_message"] = log_message
#                 pipeline_status["history_messages"].append(log_message)
#     if not all_relationships_data:
#         log_message = "Didn't extract any relationships"
#         logger.info(log_message)
#         if pipeline_status is not None:
#             async with pipeline_status_lock:
#                 pipeline_status["latest_message"] = log_message
#                 pipeline_status["history_messages"].append(log_message)

#     log_message = f"Extracted {len(all_entities_data)} entities and {len(all_relationships_data)} relationships (deduplicated)"
#     logger.info(log_message)
#     if pipeline_status is not None:
#         async with pipeline_status_lock:
#             pipeline_status["latest_message"] = log_message
#             pipeline_status["history_messages"].append(log_message)
#     verbose_debug(
#         f"New entities:{all_entities_data}, relationships:{all_relationships_data}"
#     )
#     verbose_debug(f"New relationships:{all_relationships_data}")

#     if entity_vdb is not None:
#         data_for_vdb = {
#             compute_mdhash_id(dp["entity_name"], prefix="ent-"): {
#                 "entity_name": dp["entity_name"],
#                 "entity_type": dp["entity_type"],
#                 "content": f"{dp['entity_name']}\n{dp['description']}",
#                 "source_id": dp["source_id"],
#                 "file_path": dp.get("file_path", "unknown_source"),
#             }
#             for dp in all_entities_data
#         }
#         await entity_vdb.upsert(data_for_vdb)

#     if relationships_vdb is not None:
#         data_for_vdb = {
#             compute_mdhash_id(dp["src_id"] + dp["tgt_id"], prefix="rel-"): {
#                 "src_id": dp["src_id"],
#                 "tgt_id": dp["tgt_id"],
#                 "keywords": dp["keywords"],
#                 "content": f"{dp['src_id']}\t{dp['tgt_id']}\n{dp['keywords']}\n{dp['description']}",
#                 "source_id": dp["source_id"],
#                 "file_path": dp.get("file_path", "unknown_source"),
#             }
#             for dp in all_relationships_data
#         }
#         await relationships_vdb.upsert(data_for_vdb)


# async def kg_query(
#     query: str,
#     knowledge_graph_inst: BaseGraphStorage,
#     entities_vdb: BaseVectorStorage,
#     relationships_vdb: BaseVectorStorage,
#     text_chunks_db: BaseKVStorage,
#     query_param: QueryParam,
#     global_config: dict[str, str],
#     hashing_kv: BaseKVStorage | None = None,
#     system_prompt: str | None = None,
# ) -> str | AsyncIterator[str]:
#     # Handle cache

#     db_name = type(entities_vdb).__name__
#     logger.info("db_name :", db_name)
    
#     use_model_func = (
#         query_param.model_func
#         if query_param.model_func
#         else global_config["llm_model_func"]
#     )
#     args_hash = compute_args_hash(query_param.mode, query, db_name, cache_type="query")
#     cached_response, quantized, min_val, max_val = await handle_cache(
#         hashing_kv, args_hash, query, query_param.mode, cache_type="query"
#     )
#     if cached_response is not None:
#         return cached_response

#     # Extract keywords using extract_keywords_only function which already supports conversation history
#     hl_keywords, ll_keywords = await extract_keywords_only(
#         query, query_param, global_config, hashing_kv
#     )

#     logger.debug(f"High-level keywords: {hl_keywords}")
#     logger.debug(f"Low-level  keywords: {ll_keywords}")

#     # Handle empty keywords
#     if hl_keywords == [] and ll_keywords == []:
#         logger.warning("low_level_keywords and high_level_keywords is empty")
#         return PROMPTS["fail_response"]
#     if ll_keywords == [] and query_param.mode in ["local", "hybrid"]:
#         logger.warning(
#             "low_level_keywords is empty, switching from %s mode to global mode",
#             query_param.mode,
#         )
#         query_param.mode = "global"
#     if hl_keywords == [] and query_param.mode in ["global", "hybrid"]:
#         logger.warning(
#             "high_level_keywords is empty, switching from %s mode to local mode",
#             query_param.mode,
#         )
#         query_param.mode = "local"

#     ll_keywords_str = ", ".join(ll_keywords) if ll_keywords else ""
#     hl_keywords_str = ", ".join(hl_keywords) if hl_keywords else ""

#     # Build context
#     context = await _build_query_context(
#         ll_keywords_str,
#         hl_keywords_str,
#         knowledge_graph_inst,
#         entities_vdb,
#         relationships_vdb,
#         text_chunks_db,
#         query_param,
#     )

#     if query_param.only_need_context:
#         return context
#     if context is None:
#         return PROMPTS["fail_response"]

#     # Process conversation history
#     history_context = ""
#     if query_param.conversation_history:
#         history_context = get_conversation_turns(
#             query_param.conversation_history, query_param.history_turns
#         )

#     sys_prompt_temp = system_prompt if system_prompt else PROMPTS["rag_response"]
#     sys_prompt = sys_prompt_temp.format(
#         context_data=context,
#         response_type=query_param.response_type,
#         history=history_context,
#     )

#     if query_param.only_need_prompt:
#         return sys_prompt

#     len_of_prompts = len(encode_string_by_tiktoken(query + sys_prompt))
#     logger.debug(f"[kg_query]Prompt Tokens: {len_of_prompts}")

#     response = await use_model_func(
#         query,
#         system_prompt=sys_prompt,
#         stream=query_param.stream,
#     )
#     if isinstance(response, str) and len(response) > len(sys_prompt):
#         response = (
#             response.replace(sys_prompt, "")
#             .replace("user", "")
#             .replace("model", "")
#             .replace(query, "")
#             .replace("<system>", "")
#             .replace("</system>", "")
#             .strip()
#         )

#     # Save to cache
#     await save_to_cache(
#         hashing_kv,
#         CacheData(
#             args_hash=args_hash,
#             content=response,
#             prompt=query,
#             quantized=quantized,
#             min_val=min_val,
#             max_val=max_val,
#             mode=query_param.mode,
#             cache_type="query",
#         ),
#     )
#     return response


# async def extract_keywords_only(
#     text: str,
#     param: QueryParam,
#     global_config: dict[str, str],
#     hashing_kv: BaseKVStorage | None = None,
# ) -> tuple[list[str], list[str]]:
#     """
#     Extract high-level and low-level keywords from the given 'text' using the LLM.
#     This method does NOT build the final RAG context or provide a final answer.
#     It ONLY extracts keywords (hl_keywords, ll_keywords).
#     """

#     # 1. Handle cache if needed - add cache type for keywords
#     args_hash = compute_args_hash(param.mode, text, cache_type="keywords")
#     cached_response, quantized, min_val, max_val = await handle_cache(
#         hashing_kv, args_hash, text, param.mode, cache_type="keywords"
#     )
#     if cached_response is not None:
#         try:
#             keywords_data = json.loads(cached_response)
#             return keywords_data["high_level_keywords"], keywords_data[
#                 "low_level_keywords"
#             ]
#         except (json.JSONDecodeError, KeyError):
#             logger.warning(
#                 "Invalid cache format for keywords, proceeding with extraction"
#             )

#     # 2. Build the examples
#     example_number = global_config["addon_params"].get("example_number", None)
#     if example_number and example_number < len(PROMPTS["keywords_extraction_examples"]):
#         examples = "\n".join(
#             PROMPTS["keywords_extraction_examples"][: int(example_number)]
#         )
#     else:
#         examples = "\n".join(PROMPTS["keywords_extraction_examples"])
#     language = global_config["addon_params"].get(
#         "language", PROMPTS["DEFAULT_LANGUAGE"]
#     )

#     # 3. Process conversation history
#     history_context = ""
#     if param.conversation_history:
#         history_context = get_conversation_turns(
#             param.conversation_history, param.history_turns
#         )

#     # 4. Build the keyword-extraction prompt
#     kw_prompt = PROMPTS["keywords_extraction"].format(
#         query=text, examples=examples, language=language, history=history_context
#     )

#     len_of_prompts = len(encode_string_by_tiktoken(kw_prompt))
#     logger.debug(f"[kg_query]Prompt Tokens: {len_of_prompts}")

#     # 5. Call the LLM for keyword extraction
#     use_model_func = (
#         param.model_func if param.model_func else global_config["llm_model_func"]
#     )
#     result = await use_model_func(kw_prompt, keyword_extraction=True)

#     # 6. Parse out JSON from the LLM response
#     match = re.search(r"\{.*\}", result, re.DOTALL)
#     if not match:
#         logger.error("No JSON-like structure found in the LLM respond.")
#         return [], []
#     try:
#         keywords_data = json.loads(match.group(0))
#     except json.JSONDecodeError as e:
#         logger.error(f"JSON parsing error: {e}")
#         return [], []

#     hl_keywords = keywords_data.get("high_level_keywords", [])
#     ll_keywords = keywords_data.get("low_level_keywords", [])

#     # 7. Cache only the processed keywords with cache type
#     if hl_keywords or ll_keywords:
#         cache_data = {
#             "high_level_keywords": hl_keywords,
#             "low_level_keywords": ll_keywords,
#         }
#         await save_to_cache(
#             hashing_kv,
#             CacheData(
#                 args_hash=args_hash,
#                 content=json.dumps(cache_data),
#                 prompt=text,
#                 quantized=quantized,
#                 min_val=min_val,
#                 max_val=max_val,
#                 mode=param.mode,
#                 cache_type="keywords",
#             ),
#         )
#     return hl_keywords, ll_keywords


# async def mix_kg_vector_query(
#     query: str,
#     knowledge_graph_inst: BaseGraphStorage,
#     entities_vdb: BaseVectorStorage,
#     relationships_vdb: BaseVectorStorage,
#     chunks_vdb: BaseVectorStorage,
#     text_chunks_db: BaseKVStorage,
#     query_param: QueryParam,
#     global_config: dict[str, str],
#     hashing_kv: BaseKVStorage | None = None,
#     system_prompt: str | None = None,
# ) -> str | AsyncIterator[str]:
#     """
#     Hybrid retrieval implementation combining knowledge graph and vector search.

#     This function performs a hybrid search by:
#     1. Extracting semantic information from knowledge graph
#     2. Retrieving relevant text chunks through vector similarity
#     3. Combining both results for comprehensive answer generation
#     """
#     # 1. Cache handling
#     use_model_func = (
#         query_param.model_func
#         if query_param.model_func
#         else global_config["llm_model_func"]
#     )
#     args_hash = compute_args_hash("mix", query, cache_type="query")
#     cached_response, quantized, min_val, max_val = await handle_cache(
#         hashing_kv, args_hash, query, "mix", cache_type="query"
#     )
#     if cached_response is not None:
#         return cached_response

#     # Process conversation history
#     history_context = ""
#     if query_param.conversation_history:
#         history_context = get_conversation_turns(
#             query_param.conversation_history, query_param.history_turns
#         )

#     # 2. Execute knowledge graph and vector searches in parallel
#     async def get_kg_context():
#         try:
#             # Extract keywords using extract_keywords_only function which already supports conversation history
#             hl_keywords, ll_keywords = await extract_keywords_only(
#                 query, query_param, global_config, hashing_kv
#             )

#             if not hl_keywords and not ll_keywords:
#                 logger.warning("Both high-level and low-level keywords are empty")
#                 return None

#             # Convert keyword lists to strings
#             ll_keywords_str = ", ".join(ll_keywords) if ll_keywords else ""
#             hl_keywords_str = ", ".join(hl_keywords) if hl_keywords else ""

#             # Set query mode based on available keywords
#             if not ll_keywords_str and not hl_keywords_str:
#                 return None
#             elif not ll_keywords_str:
#                 query_param.mode = "global"
#             elif not hl_keywords_str:
#                 query_param.mode = "local"
#             else:
#                 query_param.mode = "hybrid"

#             # Build knowledge graph context
#             context = await _build_query_context(
#                 ll_keywords_str,
#                 hl_keywords_str,
#                 knowledge_graph_inst,
#                 entities_vdb,
#                 relationships_vdb,
#                 text_chunks_db,
#                 query_param,
#             )

#             return context

#         except Exception as e:
#             logger.error(f"Error in get_kg_context: {str(e)}")
#             return None

#     async def get_vector_context():
#         # Consider conversation history in vector search
#         augmented_query = query
#         if history_context:
#             augmented_query = f"{history_context}\n{query}"

#         try:
#             # Reduce top_k for vector search in hybrid mode since we have structured information from KG
#             mix_topk = min(10, query_param.top_k)
#             # TODO: add ids to the query
#             results = await chunks_vdb.query(
#                 augmented_query, top_k=mix_topk, ids=query_param.ids
#             )
#             if not results:
#                 return None

#             chunks_ids = [r["id"] for r in results]
#             chunks = await text_chunks_db.get_by_ids(chunks_ids)

#             valid_chunks = []
#             for chunk, result in zip(chunks, results):
#                 if chunk is not None and "content" in chunk:
#                     # Merge chunk content and time metadata
#                     chunk_with_time = {
#                         "content": chunk["content"],
#                         "created_at": result.get("created_at", None),
#                     }
#                     valid_chunks.append(chunk_with_time)

#             if not valid_chunks:
#                 return None

#             maybe_trun_chunks = truncate_list_by_token_size(
#                 valid_chunks,
#                 key=lambda x: x["content"],
#                 max_token_size=query_param.max_token_for_text_unit,
#             )

#             if not maybe_trun_chunks:
#                 return None

#             # Include time information in content
#             formatted_chunks = []
#             for c in maybe_trun_chunks:
#                 chunk_text = "File path: " + c["file_path"] + "\n" + c["content"]
#                 if c["created_at"]:
#                     chunk_text = f"[Created at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(c['created_at']))}]\n{chunk_text}"
#                 formatted_chunks.append(chunk_text)

#             logger.debug(
#                 f"Truncate chunks from {len(chunks)} to {len(formatted_chunks)} (max tokens:{query_param.max_token_for_text_unit})"
#             )
#             return "\n--New Chunk--\n".join(formatted_chunks)
#         except Exception as e:
#             logger.error(f"Error in get_vector_context: {e}")
#             return None

#     # 3. Execute both retrievals in parallel
#     kg_context, vector_context = await asyncio.gather(
#         get_kg_context(), get_vector_context()
#     )

#     # 4. Merge contexts
#     if kg_context is None and vector_context is None:
#         return PROMPTS["fail_response"]

#     if query_param.only_need_context:
#         return {"kg_context": kg_context, "vector_context": vector_context}

#     # 5. Construct hybrid prompt
#     sys_prompt = (
#         system_prompt
#         if system_prompt
#         else PROMPTS["mix_rag_response"].format(
#             kg_context=kg_context
#             if kg_context
#             else "No relevant knowledge graph information found",
#             vector_context=vector_context
#             if vector_context
#             else "No relevant text information found",
#             response_type=query_param.response_type,
#             history=history_context,
#         )
#     )

#     if query_param.only_need_prompt:
#         return sys_prompt

#     len_of_prompts = len(encode_string_by_tiktoken(query + sys_prompt))
#     logger.debug(f"[mix_kg_vector_query]Prompt Tokens: {len_of_prompts}")

#     # 6. Generate response
#     response = await use_model_func(
#         query,
#         system_prompt=sys_prompt,
#         stream=query_param.stream,
#     )

#     # Clean up response content
#     if isinstance(response, str) and len(response) > len(sys_prompt):
#         response = (
#             response.replace(sys_prompt, "")
#             .replace("user", "")
#             .replace("model", "")
#             .replace(query, "")
#             .replace("<system>", "")
#             .replace("</system>", "")
#             .strip()
#         )

#         # 7. Save cache - Only cache after collecting complete response
#         await save_to_cache(
#             hashing_kv,
#             CacheData(
#                 args_hash=args_hash,
#                 content=response,
#                 prompt=query,
#                 quantized=quantized,
#                 min_val=min_val,
#                 max_val=max_val,
#                 mode="mix",
#                 cache_type="query",
#             ),
#         )

#     return response


# async def _build_query_context(
#     ll_keywords: str,
#     hl_keywords: str,
#     knowledge_graph_inst: BaseGraphStorage,
#     entities_vdb: BaseVectorStorage,
#     relationships_vdb: BaseVectorStorage,
#     text_chunks_db: BaseKVStorage,
#     query_param: QueryParam,
# ):
#     logger.info(f"Process {os.getpid()} buidling query context...")
#     if query_param.mode == "local":
#         entities_context, relations_context, text_units_context = await _get_node_data(
#             ll_keywords,
#             knowledge_graph_inst,
#             entities_vdb,
#             text_chunks_db,
#             query_param,
#         )
#     elif query_param.mode == "global":
#         entities_context, relations_context, text_units_context = await _get_edge_data(
#             hl_keywords,
#             knowledge_graph_inst,
#             relationships_vdb,
#             text_chunks_db,
#             query_param,
#         )
#     else:  # hybrid mode
#         ll_data, hl_data = await asyncio.gather(
#             _get_node_data(
#                 ll_keywords,
#                 knowledge_graph_inst,
#                 entities_vdb,
#                 text_chunks_db,
#                 query_param,
#             ),
#             _get_edge_data(
#                 hl_keywords,
#                 knowledge_graph_inst,
#                 relationships_vdb,
#                 text_chunks_db,
#                 query_param,
#             ),
#         )

#         (
#             ll_entities_context,
#             ll_relations_context,
#             ll_text_units_context,
#         ) = ll_data

#         (
#             hl_entities_context,
#             hl_relations_context,
#             hl_text_units_context,
#         ) = hl_data

#         entities_context, relations_context, text_units_context = combine_contexts(
#             [hl_entities_context, ll_entities_context],
#             [hl_relations_context, ll_relations_context],
#             [hl_text_units_context, ll_text_units_context],
#         )
#     # not necessary to use LLM to generate a response
#     if not entities_context.strip() and not relations_context.strip():
#         return None

#     result = f"""
#     -----Entities-----
#     ```csv
#     {entities_context}
#     ```
#     -----Relationships-----
#     ```csv
#     {relations_context}
#     ```
#     -----Sources-----
#     ```csv
#     {text_units_context}
#     ```
#     """.strip()
#     return result


# async def _get_node_data(
#     query: str,
#     knowledge_graph_inst: BaseGraphStorage,
#     entities_vdb: BaseVectorStorage,
#     text_chunks_db: BaseKVStorage,
#     query_param: QueryParam,
# ):
#     # get similar entities
#     logger.info(
#         f"Query nodes: {query}, top_k: {query_param.top_k}, cosine: {entities_vdb.cosine_better_than_threshold}"
#     )

#     results = await entities_vdb.query(
#         query, top_k=query_param.top_k, ids=query_param.ids
#     )

#     if not len(results):
#         return "", "", ""
#     # get entity information
#     node_datas, node_degrees = await asyncio.gather(
#         asyncio.gather(
#             *[knowledge_graph_inst.get_node(r["entity_name"]) for r in results]
#         ),
#         asyncio.gather(
#             *[knowledge_graph_inst.node_degree(r["entity_name"]) for r in results]
#         ),
#     )

#     if not all([n is not None for n in node_datas]):
#         logger.warning("Some nodes are missing, maybe the storage is damaged")

#     node_datas = [
#         {**n, "entity_name": k["entity_name"], "rank": d}
#         for k, n, d in zip(results, node_datas, node_degrees)
#         if n is not None
#     ]  # what is this text_chunks_db doing.  dont remember it in airvx.  check the diagram.
#     # get entitytext chunk
#     use_text_units, use_relations = await asyncio.gather(
#         _find_most_related_text_unit_from_entities(
#             node_datas, query_param, text_chunks_db, knowledge_graph_inst
#         ),
#         _find_most_related_edges_from_entities(
#             node_datas, query_param, knowledge_graph_inst
#         ),
#     )

#     len_node_datas = len(node_datas)
#     node_datas = truncate_list_by_token_size(
#         node_datas,
#         key=lambda x: x["description"] if x["description"] is not None else "",
#         max_token_size=query_param.max_token_for_local_context,
#     )
#     logger.debug(
#         f"Truncate entities from {len_node_datas} to {len(node_datas)} (max tokens:{query_param.max_token_for_local_context})"
#     )

#     logger.info(
#         f"Local query uses {len(node_datas)} entites, {len(use_relations)} relations, {len(use_text_units)} chunks"
#     )

#     # build prompt
#     entites_section_list = [
#         [
#             "id",
#             "entity",
#             "type",
#             "description",
#             "rank",
#             "created_at",
#             "file_path",
#         ]
#     ]
#     for i, n in enumerate(node_datas):
#         created_at = n.get("created_at", "UNKNOWN")
#         if isinstance(created_at, (int, float)):
#             created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created_at))

#         # Get file path from node data
#         file_path = n.get("file_path", "unknown_source")

#         entites_section_list.append(
#             [
#                 i,
#                 n["entity_name"],
#                 n.get("entity_type", "UNKNOWN"),
#                 n.get("description", "UNKNOWN"),
#                 n["rank"],
#                 created_at,
#                 file_path,
#             ]
#         )
#     entities_context = list_of_list_to_csv(entites_section_list)

#     relations_section_list = [
#         [
#             "id",
#             "source",
#             "target",
#             "description",
#             "keywords",
#             "weight",
#             "rank",
#             "created_at",
#             "file_path",
#         ]
#     ]
#     for i, e in enumerate(use_relations):
#         created_at = e.get("created_at", "UNKNOWN")
#         # Convert timestamp to readable format
#         if isinstance(created_at, (int, float)):
#             created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created_at))

#         # Get file path from edge data
#         file_path = e.get("file_path", "unknown_source")

#         relations_section_list.append(
#             [
#                 i,
#                 e["src_tgt"][0],
#                 e["src_tgt"][1],
#                 e["description"],
#                 e["keywords"],
#                 e["weight"],
#                 e["rank"],
#                 created_at,
#                 file_path,
#             ]
#         )
#     relations_context = list_of_list_to_csv(relations_section_list)

#     text_units_section_list = [["id", "content", "file_path"]]
#     for i, t in enumerate(use_text_units):
#         text_units_section_list.append([i, t["content"], t["file_path"]])
#     text_units_context = list_of_list_to_csv(text_units_section_list)
#     return entities_context, relations_context, text_units_context


# async def _find_most_related_text_unit_from_entities(
#     node_datas: list[dict],
#     query_param: QueryParam,
#     text_chunks_db: BaseKVStorage,
#     knowledge_graph_inst: BaseGraphStorage,
# ):
#     text_units = [
#         split_string_by_multi_markers(dp["source_id"], [GRAPH_FIELD_SEP])
#         for dp in node_datas
#     ]
#     edges = await asyncio.gather(
#         *[knowledge_graph_inst.get_node_edges(dp["entity_name"]) for dp in node_datas]
#     )
#     all_one_hop_nodes = set()
#     for this_edges in edges:
#         if not this_edges:
#             continue
#         all_one_hop_nodes.update([e[1] for e in this_edges])

#     all_one_hop_nodes = list(all_one_hop_nodes)
#     all_one_hop_nodes_data = await asyncio.gather(
#         *[knowledge_graph_inst.get_node(e) for e in all_one_hop_nodes]
#     )

#     # Add null check for node data
#     all_one_hop_text_units_lookup = {
#         k: set(split_string_by_multi_markers(v["source_id"], [GRAPH_FIELD_SEP]))
#         for k, v in zip(all_one_hop_nodes, all_one_hop_nodes_data)
#         if v is not None and "source_id" in v  # Add source_id check
#     }

#     all_text_units_lookup = {}
#     tasks = []

#     for index, (this_text_units, this_edges) in enumerate(zip(text_units, edges)):
#         for c_id in this_text_units:
#             if c_id not in all_text_units_lookup:
#                 all_text_units_lookup[c_id] = index
#                 tasks.append((c_id, index, this_edges))

#     results = await asyncio.gather(
#         *[text_chunks_db.get_by_id(c_id) for c_id, _, _ in tasks]
#     )

#     for (c_id, index, this_edges), data in zip(tasks, results):
#         all_text_units_lookup[c_id] = {
#             "data": data,
#             "order": index,
#             "relation_counts": 0,
#         }

#         if this_edges:
#             for e in this_edges:
#                 if (
#                     e[1] in all_one_hop_text_units_lookup
#                     and c_id in all_one_hop_text_units_lookup[e[1]]
#                 ):
#                     all_text_units_lookup[c_id]["relation_counts"] += 1

#     # Filter out None values and ensure data has content
#     all_text_units = [
#         {"id": k, **v}
#         for k, v in all_text_units_lookup.items()
#         if v is not None and v.get("data") is not None and "content" in v["data"]
#     ]

#     if not all_text_units:
#         logger.warning("No valid text units found")
#         return []

#     all_text_units = sorted(
#         all_text_units, key=lambda x: (x["order"], -x["relation_counts"])
#     )

#     all_text_units = truncate_list_by_token_size(
#         all_text_units,
#         key=lambda x: x["data"]["content"],
#         max_token_size=query_param.max_token_for_text_unit,
#     )

#     logger.debug(
#         f"Truncate chunks from {len(all_text_units_lookup)} to {len(all_text_units)} (max tokens:{query_param.max_token_for_text_unit})"
#     )

#     all_text_units = [t["data"] for t in all_text_units]
#     return all_text_units


# async def _find_most_related_edges_from_entities(
#     node_datas: list[dict],
#     query_param: QueryParam,
#     knowledge_graph_inst: BaseGraphStorage,
# ):
#     all_related_edges = await asyncio.gather(
#         *[knowledge_graph_inst.get_node_edges(dp["entity_name"]) for dp in node_datas]
#     )
#     all_edges = []
#     seen = set()

#     for this_edges in all_related_edges:
#         for e in this_edges:
#             sorted_edge = tuple(sorted(e))
#             if sorted_edge not in seen:
#                 seen.add(sorted_edge)
#                 all_edges.append(sorted_edge)

#     all_edges_pack, all_edges_degree = await asyncio.gather(
#         asyncio.gather(*[knowledge_graph_inst.get_edge(e[0], e[1]) for e in all_edges]),
#         asyncio.gather(
#             *[knowledge_graph_inst.edge_degree(e[0], e[1]) for e in all_edges]
#         ),
#     )
#     all_edges_data = [
#         {"src_tgt": k, "rank": d, **v}
#         for k, v, d in zip(all_edges, all_edges_pack, all_edges_degree)
#         if v is not None
#     ]
#     all_edges_data = sorted(
#         all_edges_data, key=lambda x: (x["rank"], x["weight"]), reverse=True
#     )
#     all_edges_data = truncate_list_by_token_size(
#         all_edges_data,
#         key=lambda x: x["description"] if x["description"] is not None else "",
#         max_token_size=query_param.max_token_for_global_context,
#     )

#     logger.debug(
#         f"Truncate relations from {len(all_edges)} to {len(all_edges_data)} (max tokens:{query_param.max_token_for_global_context})"
#     )

#     return all_edges_data


# async def _get_edge_data(
#     keywords,
#     knowledge_graph_inst: BaseGraphStorage,
#     relationships_vdb: BaseVectorStorage,
#     text_chunks_db: BaseKVStorage,
#     query_param: QueryParam,
# ):
#     logger.info(
#         f"Query edges: {keywords}, top_k: {query_param.top_k}, cosine: {relationships_vdb.cosine_better_than_threshold}"
#     )

#     results = await relationships_vdb.query(
#         keywords, top_k=query_param.top_k, ids=query_param.ids
#     )

#     if not len(results):
#         return "", "", ""

#     edge_datas, edge_degree = await asyncio.gather(
#         asyncio.gather(
#             *[knowledge_graph_inst.get_edge(r["src_id"], r["tgt_id"]) for r in results]
#         ),
#         asyncio.gather(
#             *[
#                 knowledge_graph_inst.edge_degree(r["src_id"], r["tgt_id"])
#                 for r in results
#             ]
#         ),
#     )

#     edge_datas = [
#         {
#             "src_id": k["src_id"],
#             "tgt_id": k["tgt_id"],
#             "rank": d,
#             "created_at": k.get("__created_at__", None),
#             **v,
#         }
#         for k, v, d in zip(results, edge_datas, edge_degree)
#         if v is not None
#     ]
#     edge_datas = sorted(
#         edge_datas, key=lambda x: (x["rank"], x["weight"]), reverse=True
#     )
#     edge_datas = truncate_list_by_token_size(
#         edge_datas,
#         key=lambda x: x["description"] if x["description"] is not None else "",
#         max_token_size=query_param.max_token_for_global_context,
#     )
#     use_entities, use_text_units = await asyncio.gather(
#         _find_most_related_entities_from_relationships(
#             edge_datas, query_param, knowledge_graph_inst
#         ),
#         _find_related_text_unit_from_relationships(
#             edge_datas, query_param, text_chunks_db, knowledge_graph_inst
#         ),
#     )
#     logger.info(
#         f"Global query uses {len(use_entities)} entites, {len(edge_datas)} relations, {len(use_text_units)} chunks"
#     )

#     relations_section_list = [
#         [
#             "id",
#             "source",
#             "target",
#             "description",
#             "keywords",
#             "weight",
#             "rank",
#             "created_at",
#             "file_path",
#         ]
#     ]
#     for i, e in enumerate(edge_datas):
#         created_at = e.get("created_at", "Unknown")
#         # Convert timestamp to readable format
#         if isinstance(created_at, (int, float)):
#             created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created_at))

#         # Get file path from edge data
#         file_path = e.get("file_path", "unknown_source")

#         relations_section_list.append(
#             [
#                 i,
#                 e["src_id"],
#                 e["tgt_id"],
#                 e["description"],
#                 e["keywords"],
#                 e["weight"],
#                 e["rank"],
#                 created_at,
#                 file_path,
#             ]
#         )
#     relations_context = list_of_list_to_csv(relations_section_list)

#     entites_section_list = [
#         ["id", "entity", "type", "description", "rank", "created_at", "file_path"]
#     ]
#     for i, n in enumerate(use_entities):
#         created_at = n.get("created_at", "Unknown")
#         # Convert timestamp to readable format
#         if isinstance(created_at, (int, float)):
#             created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created_at))

#         # Get file path from node data
#         file_path = n.get("file_path", "unknown_source")

#         entites_section_list.append(
#             [
#                 i,
#                 n["entity_name"],
#                 n.get("entity_type", "UNKNOWN"),
#                 n.get("description", "UNKNOWN"),
#                 n["rank"],
#                 created_at,
#                 file_path,
#             ]
#         )
#     entities_context = list_of_list_to_csv(entites_section_list)

#     text_units_section_list = [["id", "content", "file_path"]]
#     for i, t in enumerate(use_text_units):
#         text_units_section_list.append([i, t["content"], t["file_path"]])
#     text_units_context = list_of_list_to_csv(text_units_section_list)
#     return entities_context, relations_context, text_units_context


# async def _find_most_related_entities_from_relationships(
#     edge_datas: list[dict],
#     query_param: QueryParam,
#     knowledge_graph_inst: BaseGraphStorage,
# ):
#     entity_names = []
#     seen = set()

#     for e in edge_datas:
#         if e["src_id"] not in seen:
#             entity_names.append(e["src_id"])
#             seen.add(e["src_id"])
#         if e["tgt_id"] not in seen:
#             entity_names.append(e["tgt_id"])
#             seen.add(e["tgt_id"])

#     node_datas, node_degrees = await asyncio.gather(
#         asyncio.gather(
#             *[
#                 knowledge_graph_inst.get_node(entity_name)
#                 for entity_name in entity_names
#             ]
#         ),
#         asyncio.gather(
#             *[
#                 knowledge_graph_inst.node_degree(entity_name)
#                 for entity_name in entity_names
#             ]
#         ),
#     )
#     node_datas = [
#         {**n, "entity_name": k, "rank": d}
#         for k, n, d in zip(entity_names, node_datas, node_degrees)
#     ]

#     len_node_datas = len(node_datas)
#     node_datas = truncate_list_by_token_size(
#         node_datas,
#         key=lambda x: x["description"] if x["description"] is not None else "",
#         max_token_size=query_param.max_token_for_local_context,
#     )
#     logger.debug(
#         f"Truncate entities from {len_node_datas} to {len(node_datas)} (max tokens:{query_param.max_token_for_local_context})"
#     )

#     return node_datas


# async def _find_related_text_unit_from_relationships(
#     edge_datas: list[dict],
#     query_param: QueryParam,
#     text_chunks_db: BaseKVStorage,
#     knowledge_graph_inst: BaseGraphStorage,
# ):
#     text_units = [
#         split_string_by_multi_markers(dp["source_id"], [GRAPH_FIELD_SEP])
#         for dp in edge_datas
#     ]
#     all_text_units_lookup = {}

#     async def fetch_chunk_data(c_id, index):
#         if c_id not in all_text_units_lookup:
#             chunk_data = await text_chunks_db.get_by_id(c_id)
#             # Only store valid data
#             if chunk_data is not None and "content" in chunk_data:
#                 all_text_units_lookup[c_id] = {
#                     "data": chunk_data,
#                     "order": index,
#                 }

#     tasks = []
#     for index, unit_list in enumerate(text_units):
#         for c_id in unit_list:
#             tasks.append(fetch_chunk_data(c_id, index))

#     await asyncio.gather(*tasks)

#     if not all_text_units_lookup:
#         logger.warning("No valid text chunks found")
#         return []

#     all_text_units = [{"id": k, **v} for k, v in all_text_units_lookup.items()]
#     all_text_units = sorted(all_text_units, key=lambda x: x["order"])

#     # Ensure all text chunks have content
#     valid_text_units = [
#         t for t in all_text_units if t["data"] is not None and "content" in t["data"]
#     ]

#     if not valid_text_units:
#         logger.warning("No valid text chunks after filtering")
#         return []

#     truncated_text_units = truncate_list_by_token_size(
#         valid_text_units,
#         key=lambda x: x["data"]["content"],
#         max_token_size=query_param.max_token_for_text_unit,
#     )

#     logger.debug(
#         f"Truncate chunks from {len(valid_text_units)} to {len(truncated_text_units)} (max tokens:{query_param.max_token_for_text_unit})"
#     )

#     all_text_units: list[TextChunkSchema] = [t["data"] for t in truncated_text_units]

#     return all_text_units


# def combine_contexts(entities, relationships, sources):
#     # Function to extract entities, relationships, and sources from context strings
#     hl_entities, ll_entities = entities[0], entities[1]
#     hl_relationships, ll_relationships = relationships[0], relationships[1]
#     hl_sources, ll_sources = sources[0], sources[1]
#     # Combine and deduplicate the entities
#     combined_entities = process_combine_contexts(hl_entities, ll_entities)

#     # Combine and deduplicate the relationships
#     combined_relationships = process_combine_contexts(
#         hl_relationships, ll_relationships
#     )

#     # Combine and deduplicate the sources
#     combined_sources = process_combine_contexts(hl_sources, ll_sources)

#     return combined_entities, combined_relationships, combined_sources


# async def naive_query(
#     query: str,
#     chunks_vdb: BaseVectorStorage,
#     text_chunks_db: BaseKVStorage,
#     query_param: QueryParam,
#     global_config: dict[str, str],
#     hashing_kv: BaseKVStorage | None = None,
#     system_prompt: str | None = None,
# ) -> str | AsyncIterator[str]:
#     # Handle cache
#     use_model_func = (
#         query_param.model_func
#         if query_param.model_func
#         else global_config["llm_model_func"]
#     )
#     args_hash = compute_args_hash(query_param.mode, query, cache_type="query")
#     cached_response, quantized, min_val, max_val = await handle_cache(
#         hashing_kv, args_hash, query, query_param.mode, cache_type="query"
#     )
#     if cached_response is not None:
#         return cached_response

#     results = await chunks_vdb.query(
#         query, top_k=query_param.top_k, ids=query_param.ids
#     )
#     if not len(results):
#         return PROMPTS["fail_response"]

#     chunks_ids = [r["id"] for r in results]
#     chunks = await text_chunks_db.get_by_ids(chunks_ids)

#     # Filter out invalid chunks
#     valid_chunks = [
#         chunk for chunk in chunks if chunk is not None and "content" in chunk
#     ]

#     if not valid_chunks:
#         logger.warning("No valid chunks found after filtering")
#         return PROMPTS["fail_response"]

#     maybe_trun_chunks = truncate_list_by_token_size(
#         valid_chunks,
#         key=lambda x: x["content"],
#         max_token_size=query_param.max_token_for_text_unit,
#     )

#     if not maybe_trun_chunks:
#         logger.warning("No chunks left after truncation")
#         return PROMPTS["fail_response"]

#     logger.debug(
#         f"Truncate chunks from {len(chunks)} to {len(maybe_trun_chunks)} (max tokens:{query_param.max_token_for_text_unit})"
#     )

#     section = "\n--New Chunk--\n".join(
#         [
#             "File path: " + c["file_path"] + "\n" + c["content"]
#             for c in maybe_trun_chunks
#         ]
#     )

#     if query_param.only_need_context:
#         return section

#     # Process conversation history
#     history_context = ""
#     if query_param.conversation_history:
#         history_context = get_conversation_turns(
#             query_param.conversation_history, query_param.history_turns
#         )

#     sys_prompt_temp = system_prompt if system_prompt else PROMPTS["naive_rag_response"]
#     sys_prompt = sys_prompt_temp.format(
#         content_data=section,
#         response_type=query_param.response_type,
#         history=history_context,
#     )

#     if query_param.only_need_prompt:
#         return sys_prompt

#     len_of_prompts = len(encode_string_by_tiktoken(query + sys_prompt))
#     logger.debug(f"[naive_query]Prompt Tokens: {len_of_prompts}")

#     response = await use_model_func(
#         query,
#         system_prompt=sys_prompt,
#     )

#     if len(response) > len(sys_prompt):
#         response = (
#             response[len(sys_prompt) :]
#             .replace(sys_prompt, "")
#             .replace("user", "")
#             .replace("model", "")
#             .replace(query, "")
#             .replace("<system>", "")
#             .replace("</system>", "")
#             .strip()
#         )

#     # Save to cache
#     await save_to_cache(
#         hashing_kv,
#         CacheData(
#             args_hash=args_hash,
#             content=response,
#             prompt=query,
#             quantized=quantized,
#             min_val=min_val,
#             max_val=max_val,
#             mode=query_param.mode,
#             cache_type="query",
#         ),
#     )

#     return response


# async def kg_query_with_keywords(
#     query: str,
#     knowledge_graph_inst: BaseGraphStorage,
#     entities_vdb: BaseVectorStorage,
#     relationships_vdb: BaseVectorStorage,
#     text_chunks_db: BaseKVStorage,
#     query_param: QueryParam,
#     global_config: dict[str, str],
#     hashing_kv: BaseKVStorage | None = None,
# ) -> str | AsyncIterator[str]:
#     """
#     Refactored kg_query that does NOT extract keywords by itself.
#     It expects hl_keywords and ll_keywords to be set in query_param, or defaults to empty.
#     Then it uses those to build context and produce a final LLM response.
#     """

#     # ---------------------------
#     # 1) Handle potential cache for query results
#     # ---------------------------
#     use_model_func = (
#         query_param.model_func
#         if query_param.model_func
#         else global_config["llm_model_func"]
#     )
#     args_hash = compute_args_hash(query_param.mode, query, cache_type="query")
#     cached_response, quantized, min_val, max_val = await handle_cache(
#         hashing_kv, args_hash, query, query_param.mode, cache_type="query"
#     )
#     if cached_response is not None:
#         return cached_response

#     # ---------------------------
#     # 2) RETRIEVE KEYWORDS FROM query_param
#     # ---------------------------

#     # If these fields don't exist, default to empty lists/strings.
#     hl_keywords = getattr(query_param, "hl_keywords", []) or []
#     ll_keywords = getattr(query_param, "ll_keywords", []) or []

#     # If neither has any keywords, you could handle that logic here.
#     if not hl_keywords and not ll_keywords:
#         logger.warning(
#             "No keywords found in query_param. Could default to global mode or fail."
#         )
#         return PROMPTS["fail_response"]
#     if not ll_keywords and query_param.mode in ["local", "hybrid"]:
#         logger.warning("low_level_keywords is empty, switching to global mode.")
#         query_param.mode = "global"
#     if not hl_keywords and query_param.mode in ["global", "hybrid"]:
#         logger.warning("high_level_keywords is empty, switching to local mode.")
#         query_param.mode = "local"

#     # Flatten low-level and high-level keywords if needed
#     ll_keywords_flat = (
#         [item for sublist in ll_keywords for item in sublist]
#         if any(isinstance(i, list) for i in ll_keywords)
#         else ll_keywords
#     )
#     hl_keywords_flat = (
#         [item for sublist in hl_keywords for item in sublist]
#         if any(isinstance(i, list) for i in hl_keywords)
#         else hl_keywords
#     )

#     # Join the flattened lists
#     ll_keywords_str = ", ".join(ll_keywords_flat) if ll_keywords_flat else ""
#     hl_keywords_str = ", ".join(hl_keywords_flat) if hl_keywords_flat else ""

#     # ---------------------------
#     # 3) BUILD CONTEXT
#     # ---------------------------
#     context = await _build_query_context(
#         ll_keywords_str,
#         hl_keywords_str,
#         knowledge_graph_inst,
#         entities_vdb,
#         relationships_vdb,
#         text_chunks_db,
#         query_param,
#     )
#     if not context:
#         return PROMPTS["fail_response"]

#     # If only context is needed, return it
#     if query_param.only_need_context:
#         return context

#     # ---------------------------
#     # 4) BUILD THE SYSTEM PROMPT + CALL LLM
#     # ---------------------------

#     # Process conversation history
#     history_context = ""
#     if query_param.conversation_history:
#         history_context = get_conversation_turns(
#             query_param.conversation_history, query_param.history_turns
#         )

#     sys_prompt_temp = PROMPTS["rag_response"]
#     sys_prompt = sys_prompt_temp.format(
#         context_data=context,
#         response_type=query_param.response_type,
#         history=history_context,
#     )

#     if query_param.only_need_prompt:
#         return sys_prompt

#     len_of_prompts = len(encode_string_by_tiktoken(query + sys_prompt))
#     logger.debug(f"[kg_query_with_keywords]Prompt Tokens: {len_of_prompts}")

#     # 6. Generate response
#     response = await use_model_func(
#         query,
#         system_prompt=sys_prompt,
#         stream=query_param.stream,
#     )

#     # Clean up response content
#     if isinstance(response, str) and len(response) > len(sys_prompt):
#         response = (
#             response.replace(sys_prompt, "")
#             .replace("user", "")
#             .replace("model", "")
#             .replace(query, "")
#             .replace("<system>", "")
#             .replace("</system>", "")
#             .strip()
#         )

#         # 7. Save cache - 只有在收集完整响应后才缓存
#         await save_to_cache(
#             hashing_kv,
#             CacheData(
#                 args_hash=args_hash,
#                 content=response,
#                 prompt=query,
#                 quantized=quantized,
#                 min_val=min_val,
#                 max_val=max_val,
#                 mode=query_param.mode,
#                 cache_type="query",
#             ),
#         )

#     return response


# async def query_with_keywords(
#     query: str,
#     prompt: str,
#     param: QueryParam,
#     knowledge_graph_inst: BaseGraphStorage,
#     entities_vdb: BaseVectorStorage,
#     relationships_vdb: BaseVectorStorage,
#     chunks_vdb: BaseVectorStorage,
#     text_chunks_db: BaseKVStorage,
#     global_config: dict[str, str],
#     hashing_kv: BaseKVStorage | None = None,
# ) -> str | AsyncIterator[str]:
#     """
#     Extract keywords from the query and then use them for retrieving information.

#     1. Extracts high-level and low-level keywords from the query
#     2. Formats the query with the extracted keywords and prompt
#     3. Uses the appropriate query method based on param.mode

#     Args:
#         query: The user's query
#         prompt: Additional prompt to prepend to the query
#         param: Query parameters
#         knowledge_graph_inst: Knowledge graph storage
#         entities_vdb: Entities vector database
#         relationships_vdb: Relationships vector database
#         chunks_vdb: Document chunks vector database
#         text_chunks_db: Text chunks storage
#         global_config: Global configuration
#         hashing_kv: Cache storage

#     Returns:
#         Query response or async iterator
#     """
#     # Extract keywords
#     hl_keywords, ll_keywords = await extract_keywords_only(
#         text=query,
#         param=param,
#         global_config=global_config,
#         hashing_kv=hashing_kv,
#     )

#     param.hl_keywords = hl_keywords
#     param.ll_keywords = ll_keywords

#     # Create a new string with the prompt and the keywords
#     ll_keywords_str = ", ".join(ll_keywords)
#     hl_keywords_str = ", ".join(hl_keywords)
#     formatted_question = f"{prompt}\n\n### Keywords:\nHigh-level: {hl_keywords_str}\nLow-level: {ll_keywords_str}\n\n### Query:\n{query}"

#     # Use appropriate query method based on mode
#     if param.mode in ["local", "global", "hybrid"]:
#         return await kg_query_with_keywords(
#             formatted_question,
#             knowledge_graph_inst,
#             entities_vdb,
#             relationships_vdb,
#             text_chunks_db,
#             param,
#             global_config,
#             hashing_kv=hashing_kv,
#         )
#     elif param.mode == "naive":
#         return await naive_query(
#             formatted_question,
#             chunks_vdb,
#             text_chunks_db,
#             param,
#             global_config,
#             hashing_kv=hashing_kv,
#         )
#     elif param.mode == "mix":
#         return await mix_kg_vector_query(
#             formatted_question,
#             knowledge_graph_inst,
#             entities_vdb,
#             relationships_vdb,
#             chunks_vdb,
#             text_chunks_db,
#             param,
#             global_config,
#             hashing_kv=hashing_kv,
#         )
#     else:
#         raise ValueError(f"Unknown mode {param.mode}")
import asyncio
import inspect
import os
import re
from dataclasses import dataclass
from typing import Any, final, Optional
import numpy as np
import configparser


from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

import logging
from ..utils import logger
from ..base import BaseGraphStorage
from ..types import KnowledgeGraph, KnowledgeGraphNode, KnowledgeGraphEdge
import pipmaster as pm

if not pm.is_installed("neo4j"):
    pm.install("neo4j")

from neo4j import (  # type: ignore
    AsyncGraphDatabase,
    exceptions as neo4jExceptions,
    AsyncDriver,
    AsyncManagedTransaction,
    GraphDatabase,
)

config = configparser.ConfigParser()
config.read("config.ini", "utf-8")

# Get maximum number of graph nodes from environment variable, default is 1000
MAX_GRAPH_NODES = int(os.getenv("MAX_GRAPH_NODES", 1000))

# Set neo4j logger level to ERROR to suppress warning logs
logging.getLogger("neo4j").setLevel(logging.ERROR)


@final
@dataclass
class Neo4JStorage(BaseGraphStorage):
    def __init__(self, namespace, global_config, embedding_func):
        super().__init__(
            namespace=namespace,
            global_config=global_config,
            embedding_func=embedding_func,
        )
        self._driver = None
        self._driver_lock = asyncio.Lock()

        URI = os.environ.get("NEO4J_URI", config.get("neo4j", "uri", fallback=None))
        USERNAME = os.environ.get(
            "NEO4J_USERNAME", config.get("neo4j", "username", fallback=None)
        )
        PASSWORD = os.environ.get(
            "NEO4J_PASSWORD", config.get("neo4j", "password", fallback=None)
        )
        MAX_CONNECTION_POOL_SIZE = int(
            os.environ.get(
                "NEO4J_MAX_CONNECTION_POOL_SIZE",
                config.get("neo4j", "connection_pool_size", fallback=50),
            )
        )
        CONNECTION_TIMEOUT = float(
            os.environ.get(
                "NEO4J_CONNECTION_TIMEOUT",
                config.get("neo4j", "connection_timeout", fallback=30.0),
            ),
        )
        CONNECTION_ACQUISITION_TIMEOUT = float(
            os.environ.get(
                "NEO4J_CONNECTION_ACQUISITION_TIMEOUT",
                config.get("neo4j", "connection_acquisition_timeout", fallback=30.0),
            ),
        )
        MAX_TRANSACTION_RETRY_TIME = float(
            os.environ.get(
                "NEO4J_MAX_TRANSACTION_RETRY_TIME",
                config.get("neo4j", "max_transaction_retry_time", fallback=30.0),
            ),
        )
        DATABASE = os.environ.get(
            "NEO4J_DATABASE", re.sub(r"[^a-zA-Z0-9-]", "-", namespace)
        )

        self._driver: AsyncDriver = AsyncGraphDatabase.driver(
            URI,
            auth=(USERNAME, PASSWORD),
            max_connection_pool_size=MAX_CONNECTION_POOL_SIZE,
            connection_timeout=CONNECTION_TIMEOUT,
            connection_acquisition_timeout=CONNECTION_ACQUISITION_TIMEOUT,
            max_transaction_retry_time=MAX_TRANSACTION_RETRY_TIME,
        )

        # Try to connect to the database
        with GraphDatabase.driver(
            URI,
            auth=(USERNAME, PASSWORD),
            max_connection_pool_size=MAX_CONNECTION_POOL_SIZE,
            connection_timeout=CONNECTION_TIMEOUT,
            connection_acquisition_timeout=CONNECTION_ACQUISITION_TIMEOUT,
        ) as _sync_driver:
            for database in (DATABASE, None):
                self._DATABASE = database
                connected = False

                try:
                    with _sync_driver.session(database=database) as session:
                        try:
                            session.run("MATCH (n) RETURN n LIMIT 0")
                            logger.info(f"Connected to {database} at {URI}")
                            connected = True
                        except neo4jExceptions.ServiceUnavailable as e:
                            logger.error(
                                f"{database} at {URI} is not available".capitalize()
                            )
                            raise e
                except neo4jExceptions.AuthError as e:
                    logger.error(f"Authentication failed for {database} at {URI}")
                    raise e
                except neo4jExceptions.ClientError as e:
                    if e.code == "Neo.ClientError.Database.DatabaseNotFound":
                        logger.info(
                            f"{database} at {URI} not found. Try to create specified database.".capitalize()
                        )
                        try:
                            with _sync_driver.session() as session:
                                session.run(
                                    f"CREATE DATABASE `{database}` IF NOT EXISTS"
                                )
                                logger.info(f"{database} at {URI} created".capitalize())
                                connected = True
                        except (
                            neo4jExceptions.ClientError,
                            neo4jExceptions.DatabaseError,
                        ) as e:
                            if (
                                e.code
                                == "Neo.ClientError.Statement.UnsupportedAdministrationCommand"
                            ) or (
                                e.code == "Neo.DatabaseError.Statement.ExecutionFailed"
                            ):
                                if database is not None:
                                    logger.warning(
                                        "This Neo4j instance does not support creating databases. Try to use Neo4j Desktop/Enterprise version or DozerDB instead. Fallback to use the default database."
                                    )
                            if database is None:
                                logger.error(f"Failed to create {database} at {URI}")
                                raise e

                if connected:
                    break

    def __post_init__(self):
        self._node_embed_algorithms = {
            "node2vec": self._node2vec_embed,
        }

    async def close(self):
        """Close the Neo4j driver and release all resources"""
        if self._driver:
            await self._driver.close()
            self._driver = None

    async def __aexit__(self, exc_type, exc, tb):
        """Ensure driver is closed when context manager exits"""
        await self.close()

    async def index_done_callback(self) -> None:
        # Noe4J handles persistence automatically
        pass

    async def has_node(self, node_id: str) -> bool:
        """
        Check if a node with the given label exists in the database

        Args:
            node_id: Label of the node to check

        Returns:
            bool: True if node exists, False otherwise

        Raises:
            ValueError: If node_id is invalid
            Exception: If there is an error executing the query
        """
        async with self._driver.session(
            database=self._DATABASE, default_access_mode="READ"
        ) as session:
            try:
                query = "MATCH (n:base {entity_id: $entity_id}) RETURN count(n) > 0 AS node_exists"
                result = await session.run(query, entity_id=node_id)
                single_result = await result.single()
                await result.consume()  # Ensure result is fully consumed
                return single_result["node_exists"]
            except Exception as e:
                logger.error(f"Error checking node existence for {node_id}: {str(e)}")
                await result.consume()  # Ensure results are consumed even on error
                raise

    async def has_edge(self, source_node_id: str, target_node_id: str) -> bool:
        """
        Check if an edge exists between two nodes

        Args:
            source_node_id: Label of the source node
            target_node_id: Label of the target node

        Returns:
            bool: True if edge exists, False otherwise

        Raises:
            ValueError: If either node_id is invalid
            Exception: If there is an error executing the query
        """
        async with self._driver.session(
            database=self._DATABASE, default_access_mode="READ"
        ) as session:
            try:
                query = (
                    "MATCH (a:base {entity_id: $source_entity_id})-[r]-(b:base {entity_id: $target_entity_id}) "
                    "RETURN COUNT(r) > 0 AS edgeExists"
                )
                result = await session.run(
                    query,
                    source_entity_id=source_node_id,
                    target_entity_id=target_node_id,
                )
                single_result = await result.single()
                await result.consume()  # Ensure result is fully consumed
                return single_result["edgeExists"]
            except Exception as e:
                logger.error(
                    f"Error checking edge existence between {source_node_id} and {target_node_id}: {str(e)}"
                )
                await result.consume()  # Ensure results are consumed even on error
                raise

    async def get_node(self, node_id: str) -> dict[str, str] | None:
        """Get node by its label identifier.

        Args:
            node_id: The node label to look up

        Returns:
            dict: Node properties if found
            None: If node not found

        Raises:
            ValueError: If node_id is invalid
            Exception: If there is an error executing the query
        """
        async with self._driver.session(
            database=self._DATABASE, default_access_mode="READ"
        ) as session:
            try:
                query = "MATCH (n:base {entity_id: $entity_id}) RETURN n"
                result = await session.run(query, entity_id=node_id)
                try:
                    records = await result.fetch(
                        2
                    )  # Get 2 records for duplication check

                    if len(records) > 1:
                        logger.warning(
                            f"Multiple nodes found with label '{node_id}'. Using first node."
                        )
                    if records:
                        node = records[0]["n"]
                        node_dict = dict(node)
                        # Remove base label from labels list if it exists
                        if "labels" in node_dict:
                            node_dict["labels"] = [
                                label
                                for label in node_dict["labels"]
                                if label != "base"
                            ]
                        logger.debug(f"Neo4j query node {query} return: {node_dict}")
                        return node_dict
                    return None
                finally:
                    await result.consume()  # Ensure result is fully consumed
            except Exception as e:
                logger.error(f"Error getting node for {node_id}: {str(e)}")
                raise

    async def node_degree(self, node_id: str) -> int:
        """Get the degree (number of relationships) of a node with the given label.
        If multiple nodes have the same label, returns the degree of the first node.
        If no node is found, returns 0.

        Args:
            node_id: The label of the node

        Returns:
            int: The number of relationships the node has, or 0 if no node found

        Raises:
            ValueError: If node_id is invalid
            Exception: If there is an error executing the query
        """
        async with self._driver.session(
            database=self._DATABASE, default_access_mode="READ"
        ) as session:
            try:
                query = """
                    MATCH (n:base {entity_id: $entity_id})
                    OPTIONAL MATCH (n)-[r]-()
                    RETURN COUNT(r) AS degree
                """
                result = await session.run(query, entity_id=node_id)
                try:
                    record = await result.single()

                    if not record:
                        logger.warning(f"No node found with label '{node_id}'")
                        return 0

                    degree = record["degree"]
                    logger.debug(
                        "Neo4j query node degree for {node_id} return: {degree}"
                    )
                    return degree
                finally:
                    await result.consume()  # Ensure result is fully consumed
            except Exception as e:
                logger.error(f"Error getting node degree for {node_id}: {str(e)}")
                raise
    async def get_nodes_bulk(self, entity_ids: list[str]) -> dict[str, dict]:
        query = """
        UNWIND $ids AS id
        MATCH (n:base {entity_id: id})
        RETURN id, n
        """
        async with self._driver.session(database=self._DATABASE) as session:
            result = await session.run(query, ids=entity_ids)
            records = await result.data()
            return {r["id"]: dict(r["n"]) for r in records}


    async def get_edges_bulk(
        self, edge_pairs: list[tuple[str, str]]
    ) -> dict[tuple[str, str], dict]:
        """Fetch properties of edges in bulk between multiple (source, target) node pairs.

        Args:
            edge_pairs: List of (source_node_id, target_node_id) tuples.

        Returns:
            Dictionary mapping (source, target) to edge property dicts.
        """
        if not edge_pairs:
            return {}

        try:
            query = """
            UNWIND $pairs AS pair
            MATCH (a:base {entity_id: pair[0]})-[r]-(b:base {entity_id: pair[1]})
            RETURN pair, properties(r) AS edge_properties
            """
            async with self._driver.session(database=self._DATABASE, default_access_mode="READ") as session:
                result = await session.run(query, pairs=edge_pairs)
                try:
                    records = await result.data()
                    edge_map = {}

                    for r in records:
                        try:
                            pair = tuple(r.get("pair", []))  # Should be 2-length
                            props = dict(r.get("edge_properties", {}))

                            # Validate pair
                            if len(pair) != 2:
                                logger.warning(f"Skipping malformed pair: {pair}")
                                continue

                            # Ensure required keys with defaults
                            required_keys = {
                                "weight": 0.0,
                                "source_id": None,
                                "description": None,
                                "keywords": None,
                            }
                            for key, default_value in required_keys.items():
                                if key not in props:
                                    props[key] = default_value
                                    logger.warning(
                                        f"Edge {pair} missing '{key}', defaulting to {default_value}"
                                    )

                            edge_map[pair] = props
                        except Exception as e:
                            logger.error(f"Error processing record {r}: {e}")

                    return edge_map
                finally:
                    await result.consume()

        except Exception as e:
            logger.error(f"Error in get_edges_bulk: {e}")
            raise




    async def edge_degree(self, src_id: str, tgt_id: str) -> int:
        """Get the total degree (sum of relationships) of two nodes.

        Args:
            src_id: Label of the source node
            tgt_id: Label of the target node

        Returns:
            int: Sum of the degrees of both nodes
        """
        src_degree = await self.node_degree(src_id)
        trg_degree = await self.node_degree(tgt_id)

        # Convert None to 0 for addition
        src_degree = 0 if src_degree is None else src_degree
        trg_degree = 0 if trg_degree is None else trg_degree

        degrees = int(src_degree) + int(trg_degree)
        return degrees

    async def get_edge(
        self, source_node_id: str, target_node_id: str
    ) -> dict[str, str] | None:
        """Get edge properties between two nodes.

        Args:
            source_node_id: Label of the source node
            target_node_id: Label of the target node

        Returns:
            dict: Edge properties if found, default properties if not found or on error

        Raises:
            ValueError: If either node_id is invalid
            Exception: If there is an error executing the query
        """
        try:
            async with self._driver.session(
                database=self._DATABASE, default_access_mode="READ"
            ) as session:
                query = """
                MATCH (start:base {entity_id: $source_entity_id})-[r]-(end:base {entity_id: $target_entity_id})
                RETURN properties(r) as edge_properties
                """
                result = await session.run(
                    query,
                    source_entity_id=source_node_id,
                    target_entity_id=target_node_id,
                )
                try:
                    records = await result.fetch(2)

                    if len(records) > 1:
                        logger.warning(
                            f"Multiple edges found between '{source_node_id}' and '{target_node_id}'. Using first edge."
                        )
                    if records:
                        try:
                            edge_result = dict(records[0]["edge_properties"])
                            logger.debug(f"Result: {edge_result}")
                            # Ensure required keys exist with defaults
                            required_keys = {
                                "weight": 0.0,
                                "source_id": None,
                                "description": None,
                                "keywords": None,
                            }
                            for key, default_value in required_keys.items():
                                if key not in edge_result:
                                    edge_result[key] = default_value
                                    logger.warning(
                                        f"Edge between {source_node_id} and {target_node_id} "
                                        f"missing {key}, using default: {default_value}"
                                    )

                            logger.debug(
                                f"{inspect.currentframe().f_code.co_name}:query:{query}:result:{edge_result}"
                            )
                            return edge_result
                        except (KeyError, TypeError, ValueError) as e:
                            logger.error(
                                f"Error processing edge properties between {source_node_id} "
                                f"and {target_node_id}: {str(e)}"
                            )
                            # Return default edge properties on error
                            return {
                                "weight": 0.0,
                                "source_id": None,
                                "description": None,
                                "keywords": None,
                            }

                    logger.debug(
                        f"{inspect.currentframe().f_code.co_name}: No edge found between {source_node_id} and {target_node_id}"
                    )
                    # Return default edge properties when no edge found
                    return {
                        "weight": 0.0,
                        "source_id": None,
                        "description": None,
                        "keywords": None,
                    }
                finally:
                    await result.consume()  # Ensure result is fully consumed

        except Exception as e:
            logger.error(
                f"Error in get_edge between {source_node_id} and {target_node_id}: {str(e)}"
            )
            raise

    async def get_node_edges(self, source_node_id: str) -> list[tuple[str, str]] | None:
        """Retrieves all edges (relationships) for a particular node identified by its label.

        Args:
            source_node_id: Label of the node to get edges for

        Returns:
            list[tuple[str, str]]: List of (source_label, target_label) tuples representing edges
            None: If no edges found

        Raises:
            ValueError: If source_node_id is invalid
            Exception: If there is an error executing the query
        """
        try:
            async with self._driver.session(
                database=self._DATABASE, default_access_mode="READ"
            ) as session:
                try:
                    query = """MATCH (n:base {entity_id: $entity_id})
                            OPTIONAL MATCH (n)-[r]-(connected:base)
                            WHERE connected.entity_id IS NOT NULL
                            RETURN n, r, connected"""
                    results = await session.run(query, entity_id=source_node_id)

                    edges = []
                    async for record in results:
                        source_node = record["n"]
                        connected_node = record["connected"]

                        # Skip if either node is None
                        if not source_node or not connected_node:
                            continue

                        source_label = (
                            source_node.get("entity_id")
                            if source_node.get("entity_id")
                            else None
                        )
                        target_label = (
                            connected_node.get("entity_id")
                            if connected_node.get("entity_id")
                            else None
                        )

                        if source_label and target_label:
                            edges.append((source_label, target_label))

                    await results.consume()  # Ensure results are consumed
                    return edges
                except Exception as e:
                    logger.error(
                        f"Error getting edges for node {source_node_id}: {str(e)}"
                    )
                    await results.consume()  # Ensure results are consumed even on error
                    raise
        except Exception as e:
            logger.error(f"Error in get_node_edges for {source_node_id}: {str(e)}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(
            (
                neo4jExceptions.ServiceUnavailable,
                neo4jExceptions.TransientError,
                neo4jExceptions.WriteServiceUnavailable,
                neo4jExceptions.ClientError,
            )
        ),
    )
    async def upsert_node(self, node_id: str, node_data: dict[str, str]) -> None:
        """
        Upsert a node in the Neo4j database.

        Args:
            node_id: The unique identifier for the node (used as label)
            node_data: Dictionary of node properties
        """
        properties = node_data
        entity_type = properties["entity_type"]
        entity_id = properties["entity_id"]
        if "entity_id" not in properties:
            raise ValueError("Neo4j: node properties must contain an 'entity_id' field")

        try:
            async with self._driver.session(database=self._DATABASE) as session:

                async def execute_upsert(tx: AsyncManagedTransaction):
                    query = (
                        """
                    MERGE (n:base {entity_id: $properties.entity_id})
                    SET n += $properties
                    SET n:`%s`
                    """
                        % entity_type
                    )
                    result = await tx.run(query, properties=properties)
                    logger.debug(
                        f"Upserted node with entity_id '{entity_id}' and properties: {properties}"
                    )
                    await result.consume()  # Ensure result is fully consumed

                await session.execute_write(execute_upsert)
        except Exception as e:
            logger.error(f"Error during upsert: {str(e)}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(
            (
                neo4jExceptions.ServiceUnavailable,
                neo4jExceptions.TransientError,
                neo4jExceptions.WriteServiceUnavailable,
                neo4jExceptions.ClientError,
            )
        ),
    )
    async def upsert_nodes_batch(self, nodes: list[dict[str, str]]) -> None:
        """
        Batch upsert nodes into Neo4j using UNWIND for high performance.
        Each node must include 'entity_id' and 'entity_type'.
        """
        query = """
        UNWIND $nodes AS node
        MERGE (n:base {entity_id: node.entity_id})
        SET n += node
        SET n:`${entity_type}`
        """

        # Prepare data and entity type labels
        for node in nodes:
            if "entity_id" not in node:
                raise ValueError("Each node must have 'entity_id'")
            if "entity_type" not in node:
                node["entity_type"] = "base"

        try:
            async with self._driver.session(database=self._DATABASE) as session:
                await session.execute_write(
                    lambda tx: tx.run(query, nodes=nodes)
                )
        except Exception as e:
            logger.error(f"Batch upsert failed: {e}")
            raise

    async def upsert_edge(
        self, source_node_id: str, target_node_id: str, edge_data: dict[str, str]
    ) -> None:
        """
        Upsert an edge and its properties between two nodes identified by their labels.
        Ensures both source and target nodes exist and are unique before creating the edge.
        Uses entity_id property to uniquely identify nodes.

        Args:
            source_node_id (str): Label of the source node (used as identifier)
            target_node_id (str): Label of the target node (used as identifier)
            edge_data (dict): Dictionary of properties to set on the edge

        Raises:
            ValueError: If either source or target node does not exist or is not unique
        """
        try:
            edge_properties = edge_data
            async with self._driver.session(database=self._DATABASE) as session:

                async def execute_upsert(tx: AsyncManagedTransaction):
                    query = """
                    MATCH (source:base {entity_id: $source_entity_id})
                    WITH source
                    MATCH (target:base {entity_id: $target_entity_id})
                    MERGE (source)-[r:DIRECTED]-(target)
                    SET r += $properties
                    RETURN r, source, target
                    """
                    result = await tx.run(
                        query,
                        source_entity_id=source_node_id,
                        target_entity_id=target_node_id,
                        properties=edge_properties,
                    )
                    try:
                        records = await result.fetch(2)
                        if records:
                            logger.debug(
                                f"Upserted edge from '{source_node_id}' to '{target_node_id}'"
                                f"with properties: {edge_properties}"
                            )
                    finally:
                        await result.consume()  # Ensure result is consumed

                await session.execute_write(execute_upsert)
        except Exception as e:
            logger.error(f"Error during edge upsert: {str(e)}")
            raise

    async def upsert_edges_batch(self, edges: list[dict]) -> None:
        try:
            async with self._driver.session(database=self._DATABASE) as session:

                async def execute_batch(tx: AsyncManagedTransaction):
                    logger.info(f"\033[1;32m✔️  Batch upsert edges with {len(edges)} edges\033[0m")
                    for edge in edges:
                        src_id = edge["src_id"]
                        tgt_id = edge["tgt_id"]
                        edge_data = edge["edge_data"]

                        query = """
                        MATCH (source:base {entity_id: $source_entity_id})
                        WITH source
                        MATCH (target:base {entity_id: $target_entity_id})
                        MERGE (source)-[r:DIRECTED]-(target)
                        SET r += $properties
                        RETURN r
                        """
                        await tx.run(
                            query,
                            source_entity_id=src_id,
                            target_entity_id=tgt_id,
                            properties=edge_data,
                        )

                await session.execute_write(execute_batch)
        except Exception as e:
            logger.error(f"Error during edge batch upsert: {str(e)}")
            raise

    async def _node2vec_embed(self):
        print("Implemented but never called.")

    async def get_knowledge_graph(
        self,
        node_label: str,
        max_depth: int = 3,
        min_degree: int = 0,
        inclusive: bool = False,
    ) -> KnowledgeGraph:
        """
        Retrieve a connected subgraph of nodes where the label includes the specified `node_label`.
        Maximum number of nodes is constrained by the environment variable `MAX_GRAPH_NODES` (default: 1000).
        When reducing the number of nodes, the prioritization criteria are as follows:
            1. min_degree does not affect nodes directly connected to the matching nodes
            2. Label matching nodes take precedence
            3. Followed by nodes directly connected to the matching nodes
            4. Finally, the degree of the nodes

        Args:
            node_label: Label of the starting node
            max_depth: Maximum depth of the subgraph
            min_degree: Minimum degree of nodes to include. Defaults to 0
            inclusive: Do an inclusive search if true
        Returns:
            KnowledgeGraph: Complete connected subgraph for specified node
        """
        result = KnowledgeGraph()
        seen_nodes = set()
        seen_edges = set()

        async with self._driver.session(
            database=self._DATABASE, default_access_mode="READ"
        ) as session:
            try:
                if node_label == "*":
                    main_query = """
                    MATCH (n)
                    OPTIONAL MATCH (n)-[r]-()
                    WITH n, COALESCE(count(r), 0) AS degree
                    WHERE degree >= $min_degree
                    ORDER BY degree DESC
                    LIMIT $max_nodes
                    WITH collect({node: n}) AS filtered_nodes
                    UNWIND filtered_nodes AS node_info
                    WITH collect(node_info.node) AS kept_nodes, filtered_nodes
                    OPTIONAL MATCH (a)-[r]-(b)
                    WHERE a IN kept_nodes AND b IN kept_nodes
                    RETURN filtered_nodes AS node_info,
                           collect(DISTINCT r) AS relationships
                    """
                    result_set = await session.run(
                        main_query,
                        {"max_nodes": MAX_GRAPH_NODES, "min_degree": min_degree},
                    )

                else:
                    # Main query uses partial matching
                    main_query = """
                    MATCH (start)
                    WHERE
                        CASE
                            WHEN $inclusive THEN start.entity_id CONTAINS $entity_id
                            ELSE start.entity_id = $entity_id
                        END
                    WITH start
                    CALL apoc.path.subgraphAll(start, {
                        relationshipFilter: '',
                        minLevel: 0,
                        maxLevel: $max_depth,
                        bfs: true
                    })
                    YIELD nodes, relationships
                    WITH start, nodes, relationships
                    UNWIND nodes AS node
                    OPTIONAL MATCH (node)-[r]-()
                    WITH node, COALESCE(count(r), 0) AS degree, start, nodes, relationships
                    WHERE node = start OR EXISTS((start)--(node)) OR degree >= $min_degree
                    ORDER BY
                        CASE
                            WHEN node = start THEN 3
                            WHEN EXISTS((start)--(node)) THEN 2
                            ELSE 1
                        END DESC,
                        degree DESC
                    LIMIT $max_nodes
                    WITH collect({node: node}) AS filtered_nodes
                    UNWIND filtered_nodes AS node_info
                    WITH collect(node_info.node) AS kept_nodes, filtered_nodes
                    OPTIONAL MATCH (a)-[r]-(b)
                    WHERE a IN kept_nodes AND b IN kept_nodes
                    RETURN filtered_nodes AS node_info,
                           collect(DISTINCT r) AS relationships
                    """
                    result_set = await session.run(
                        main_query,
                        {
                            "max_nodes": MAX_GRAPH_NODES,
                            "entity_id": node_label,
                            "inclusive": inclusive,
                            "max_depth": max_depth,
                            "min_degree": min_degree,
                        },
                    )

                try:
                    record = await result_set.single()

                    if record:
                        # Handle nodes (compatible with multi-label cases)
                        for node_info in record["node_info"]:
                            node = node_info["node"]
                            node_id = node.id
                            if node_id not in seen_nodes:
                                result.nodes.append(
                                    KnowledgeGraphNode(
                                        id=f"{node_id}",
                                        labels=[node.get("entity_id")],
                                        properties=dict(node),
                                    )
                                )
                                seen_nodes.add(node_id)

                        # Handle relationships (including direction information)
                        for rel in record["relationships"]:
                            edge_id = rel.id
                            if edge_id not in seen_edges:
                                start = rel.start_node
                                end = rel.end_node
                                result.edges.append(
                                    KnowledgeGraphEdge(
                                        id=f"{edge_id}",
                                        type=rel.type,
                                        source=f"{start.id}",
                                        target=f"{end.id}",
                                        properties=dict(rel),
                                    )
                                )
                                seen_edges.add(edge_id)

                        logger.info(
                            f"Process {os.getpid()} graph query return: {len(result.nodes)} nodes, {len(result.edges)} edges"
                        )
                finally:
                    await result_set.consume()  # Ensure result set is consumed

            except neo4jExceptions.ClientError as e:
                logger.warning(f"APOC plugin error: {str(e)}")
                if node_label != "*":
                    logger.warning(
                        "Neo4j: falling back to basic Cypher recursive search..."
                    )
                    if inclusive:
                        logger.warning(
                            "Neo4j: inclusive search mode is not supported in recursive query, using exact matching"
                        )
                    return await self._robust_fallback(
                        node_label, max_depth, min_degree
                    )

        return result

    async def _robust_fallback(
        self, node_label: str, max_depth: int, min_degree: int = 0
    ) -> KnowledgeGraph:
        """
        Fallback implementation when APOC plugin is not available or incompatible.
        This method implements the same functionality as get_knowledge_graph but uses
        only basic Cypher queries and recursive traversal instead of APOC procedures.
        """
        result = KnowledgeGraph()
        visited_nodes = set()
        visited_edges = set()

        async def traverse(
            node: KnowledgeGraphNode,
            edge: Optional[KnowledgeGraphEdge],
            current_depth: int,
        ):
            # Check traversal limits
            if current_depth > max_depth:
                logger.debug(f"Reached max depth: {max_depth}")
                return
            if len(visited_nodes) >= MAX_GRAPH_NODES:
                logger.debug(f"Reached max nodes limit: {MAX_GRAPH_NODES}")
                return

            # Check if node already visited
            if node.id in visited_nodes:
                return

            # Get all edges and target nodes
            async with self._driver.session(
                database=self._DATABASE, default_access_mode="READ"
            ) as session:
                query = """
                MATCH (a:base {entity_id: $entity_id})-[r]-(b)
                WITH r, b, id(r) as edge_id, id(b) as target_id
                RETURN r, b, edge_id, target_id
                """
                results = await session.run(query, entity_id=node.id)

                # Get all records and release database connection
                records = await results.fetch(
                    1000
                )  # Max neighbour nodes we can handled
                await results.consume()  # Ensure results are consumed

                # Nodes not connected to start node need to check degree
                if current_depth > 1 and len(records) < min_degree:
                    return

                # Add current node to result
                result.nodes.append(node)
                visited_nodes.add(node.id)

                # Add edge to result if it exists and not already added
                if edge and edge.id not in visited_edges:
                    result.edges.append(edge)
                    visited_edges.add(edge.id)

                # Prepare nodes and edges for recursive processing
                nodes_to_process = []
                for record in records:
                    rel = record["r"]
                    edge_id = str(record["edge_id"])
                    if edge_id not in visited_edges:
                        b_node = record["b"]
                        target_id = b_node.get("entity_id")

                        if target_id:  # Only process if target node has entity_id
                            # Create KnowledgeGraphNode for target
                            target_node = KnowledgeGraphNode(
                                id=f"{target_id}",
                                labels=list(f"{target_id}"),
                                properties=dict(b_node.properties),
                            )

                            # Create KnowledgeGraphEdge
                            target_edge = KnowledgeGraphEdge(
                                id=f"{edge_id}",
                                type=rel.type,
                                source=f"{node.id}",
                                target=f"{target_id}",
                                properties=dict(rel),
                            )

                            nodes_to_process.append((target_node, target_edge))
                        else:
                            logger.warning(
                                f"Skipping edge {edge_id} due to missing labels on target node"
                            )

                # Process nodes after releasing database connection
                for target_node, target_edge in nodes_to_process:
                    await traverse(target_node, target_edge, current_depth + 1)

        # Get the starting node's data
        async with self._driver.session(
            database=self._DATABASE, default_access_mode="READ"
        ) as session:
            query = """
            MATCH (n:base {entity_id: $entity_id})
            RETURN id(n) as node_id, n
            """
            node_result = await session.run(query, entity_id=node_label)
            try:
                node_record = await node_result.single()
                if not node_record:
                    return result

                # Create initial KnowledgeGraphNode
                start_node = KnowledgeGraphNode(
                    id=f"{node_record['n'].get('entity_id')}",
                    labels=list(f"{node_record['n'].get('entity_id')}"),
                    properties=dict(node_record["n"].properties),
                )
            finally:
                await node_result.consume()  # Ensure results are consumed

            # Start traversal with the initial node
            await traverse(start_node, None, 0)

        return result

    async def get_all_labels(self) -> list[str]:
        """
        Get all existing node labels in the database
        Returns:
            ["Person", "Company", ...]  # Alphabetically sorted label list
        """
        async with self._driver.session(
            database=self._DATABASE, default_access_mode="READ"
        ) as session:
            # Method 1: Direct metadata query (Available for Neo4j 4.3+)
            # query = "CALL db.labels() YIELD label RETURN label"

            # Method 2: Query compatible with older versions
            query = """
            MATCH (n)
            WHERE n.entity_id IS NOT NULL
            RETURN DISTINCT n.entity_id AS label
            ORDER BY label
            """
            result = await session.run(query)
            labels = []
            try:
                async for record in result:
                    labels.append(record["label"])
            finally:
                await (
                    result.consume()
                )  # Ensure results are consumed even if processing fails
            return labels

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(
            (
                neo4jExceptions.ServiceUnavailable,
                neo4jExceptions.TransientError,
                neo4jExceptions.WriteServiceUnavailable,
                neo4jExceptions.ClientError,
            )
        ),
    )
    async def delete_node(self, node_id: str) -> None:
        """Delete a node with the specified label

        Args:
            node_id: The label of the node to delete
        """

        async def _do_delete(tx: AsyncManagedTransaction):
            query = """
            MATCH (n:base {entity_id: $entity_id})
            DETACH DELETE n
            """
            result = await tx.run(query, entity_id=node_id)
            logger.debug(f"Deleted node with label '{node_id}'")
            await result.consume()  # Ensure result is fully consumed

        try:
            async with self._driver.session(database=self._DATABASE) as session:
                await session.execute_write(_do_delete)
        except Exception as e:
            logger.error(f"Error during node deletion: {str(e)}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(
            (
                neo4jExceptions.ServiceUnavailable,
                neo4jExceptions.TransientError,
                neo4jExceptions.WriteServiceUnavailable,
                neo4jExceptions.ClientError,
            )
        ),
    )
    async def remove_nodes(self, nodes: list[str]):
        """Delete multiple nodes

        Args:
            nodes: List of node labels to be deleted
        """
        for node in nodes:
            await self.delete_node(node)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(
            (
                neo4jExceptions.ServiceUnavailable,
                neo4jExceptions.TransientError,
                neo4jExceptions.WriteServiceUnavailable,
                neo4jExceptions.ClientError,
            )
        ),
    )
    async def remove_edges(self, edges: list[tuple[str, str]]):
        """Delete multiple edges

        Args:
            edges: List of edges to be deleted, each edge is a (source, target) tuple
        """
        for source, target in edges:

            async def _do_delete_edge(tx: AsyncManagedTransaction):
                query = """
                MATCH (source:base {entity_id: $source_entity_id})-[r]-(target:base {entity_id: $target_entity_id})
                DELETE r
                """
                result = await tx.run(
                    query, source_entity_id=source, target_entity_id=target
                )
                logger.debug(f"Deleted edge from '{source}' to '{target}'")
                await result.consume()  # Ensure result is fully consumed

            try:
                async with self._driver.session(database=self._DATABASE) as session:
                    await session.execute_write(_do_delete_edge)
            except Exception as e:
                logger.error(f"Error during edge deletion: {str(e)}")
                raise

    async def embed_nodes(
        self, algorithm: str
    ) -> tuple[np.ndarray[Any, Any], list[str]]:
        raise NotImplementedError
