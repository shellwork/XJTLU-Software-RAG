# Project Introduction


### iGEM

The full name of [iGEM](https://igem.org/) is “International Genetically Engineered Machine Competition”. It is a global synthetic biology competition aimed at encouraging students to design and build genetic engineering projects to solve real-world problems through teamwork and scientific innovation. 


## Project Overview

The iGEM Parts Registry is a large open database of DNA elements contributed by iGEM teams over the years. However, the data quality is inconsistent, with many parts lacking proper descriptions, optimization, or contributions. Additionally, the current presentation of results lacks clear indexing and quick search functions, making it difficult to efficiently access and summarize information.

ChatParts is an AI agent designed to improve productivity by organizing and retrieving parts as well as experiment and protocol information using a **RAG (Retrieval-Augmented Generation) system**. Fine-tuning enhances the model's performance in specific domains, while the iGEM ChatParts Community platform helps promote and expand the project's reach.

## Model Construction

Retrieval-augmented generation (RAG) combines information retrieval and generation models. When a user uploads a PDF, it's converted to text and split into chunks, which are then embedded into vector representations stored in a VectorStore. When a prompt is entered, it's vectorized and compared to the stored vectors to find relevant text chunks. These chunks are then used to create a prompt for a Large Language Model (LLM), generating a final answer. This process enhances the accuracy and relevance of the generated content.

![RAG Model](https://static.igem.wiki/teams/5256/model/model2.png)

1. Centralized Data Management: Organize biological data into a structured knowledge base.
2. Efficient Information Retrieval: Implement a system for rapid, targeted searches.
3. Data Augmentation: Use AI-driven tools to process and classify biological parts for easier accessibility and utility.
4. RAG-based System: Integrate a Retrieval-Augmented Generation (RAG) system to enhance the querying and information    management experience.
::: tip
**More information can be found on our *[team wiki](https://2024.igem.wiki/xjtlu-software/)*.**
:::

## Problems Encountered in Research

::: warning
Data Privacy and Security
:::

Researchers face significant challenges regarding data privacy breaches. Concerns over sensitive data being exposed or accessed without permission are common, especially when shared over public networks. Many research institutions use intranets or secure, closed networks to maintain better control and minimize the risk of data leakage. Due to concerns about losing confidentiality, researchers often avoid using websites like GPT to prevent private documents from being uploaded to external servers.

::: tip
Customizable Knowledge Base
:::

Researchers often find that large models, while having strong generalization abilities, lack the depth of domain-specific knowledge required for their specialized work. These models may provide broad insights, but their responses can be too superficial or imprecise when addressing highly technical or niche topics. This limits their usefulness in research, where deep expertise and accurate, detailed information are essential.


## Offline Software Package

We took these situations into account and developed an offline package designed to meet the unique needs of researchers concerned about data privacy and security. This package empowers users to create their own private knowledge bases tailored to their specific requirements. With this tool, users have complete control over the content, allowing them to curate and manage information without the fear of data leakage or unauthorized access. Furthermore, the package is built on open-source software, enabling users to modify and customize it according to their individual needs. This flexibility ensures that researchers can adapt the tool to their workflows, enhancing both productivity and confidence in their data management practices.
::: tip
This document focuses on the introduction and use of local software packages developed by our team. 
:::



