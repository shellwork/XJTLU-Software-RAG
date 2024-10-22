import{_ as t,c as a,a0 as i,o}from"./chunks/framework.DgZgdyI2.js";const u=JSON.parse('{"title":"Project Introduction","description":"","frontmatter":{},"headers":[],"relativePath":"docs/project-introduction.md","filePath":"docs/project-introduction.md"}'),n={name:"docs/project-introduction.md"};function r(s,e,c,l,d,h){return o(),a("div",null,e[0]||(e[0]=[i('<h1 id="project-introduction" tabindex="-1">Project Introduction <a class="header-anchor" href="#project-introduction" aria-label="Permalink to &quot;Project Introduction&quot;">​</a></h1><h3 id="igem" tabindex="-1">iGEM <a class="header-anchor" href="#igem" aria-label="Permalink to &quot;iGEM&quot;">​</a></h3><p>The full name of <a href="https://igem.org/" target="_blank" rel="noreferrer">iGEM</a> is “International Genetically Engineered Machine Competition”. It is a global synthetic biology competition aimed at encouraging students to design and build genetic engineering projects to solve real-world problems through teamwork and scientific innovation.</p><h2 id="project-overview" tabindex="-1">Project Overview <a class="header-anchor" href="#project-overview" aria-label="Permalink to &quot;Project Overview&quot;">​</a></h2><p>The iGEM Parts Registry is a large open database of DNA elements contributed by iGEM teams over the years. However, the data quality is inconsistent, with many parts lacking proper descriptions, optimization, or contributions. Additionally, the current presentation of results lacks clear indexing and quick search functions, making it difficult to efficiently access and summarize information.</p><p>ChatParts is an AI agent designed to improve productivity by organizing and retrieving parts as well as experiment and protocol information using a <strong>RAG (Retrieval-Augmented Generation) system</strong>. Fine-tuning enhances the model&#39;s performance in specific domains, while the iGEM ChatParts Community platform helps promote and expand the project&#39;s reach.</p><h2 id="model-construction" tabindex="-1">Model Construction <a class="header-anchor" href="#model-construction" aria-label="Permalink to &quot;Model Construction&quot;">​</a></h2><p>Retrieval-augmented generation (RAG) combines information retrieval and generation models. When a user uploads a PDF, it&#39;s converted to text and split into chunks, which are then embedded into vector representations stored in a VectorStore. When a prompt is entered, it&#39;s vectorized and compared to the stored vectors to find relevant text chunks. These chunks are then used to create a prompt for a Large Language Model (LLM), generating a final answer. This process enhances the accuracy and relevance of the generated content.</p><p><img src="https://static.igem.wiki/teams/5256/model/model2.png" alt="RAG Model"></p><ol><li>Centralized Data Management: Organize biological data into a structured knowledge base.</li><li>Efficient Information Retrieval: Implement a system for rapid, targeted searches.</li><li>Data Augmentation: Use AI-driven tools to process and classify biological parts for easier accessibility and utility.</li><li>RAG-based System: Integrate a Retrieval-Augmented Generation (RAG) system to enhance the querying and information management experience.</li></ol><div class="tip custom-block"><p class="custom-block-title">TIP</p><p><strong>More information can be found on our <em><a href="https://2024.igem.wiki/xjtlu-software/" target="_blank" rel="noreferrer">team wiki</a></em>.</strong></p></div><h2 id="problems-encountered-in-research" tabindex="-1">Problems Encountered in Research <a class="header-anchor" href="#problems-encountered-in-research" aria-label="Permalink to &quot;Problems Encountered in Research&quot;">​</a></h2><div class="warning custom-block"><p class="custom-block-title">WARNING</p><p>Data Privacy and Security</p></div><p>Researchers face significant challenges regarding data privacy breaches. Concerns over sensitive data being exposed or accessed without permission are common, especially when shared over public networks. Many research institutions use intranets or secure, closed networks to maintain better control and minimize the risk of data leakage. Due to concerns about losing confidentiality, researchers often avoid using websites like GPT to prevent private documents from being uploaded to external servers.</p><div class="tip custom-block"><p class="custom-block-title">TIP</p><p>Customizable Knowledge Base</p></div><p>Researchers often find that large models, while having strong generalization abilities, lack the depth of domain-specific knowledge required for their specialized work. These models may provide broad insights, but their responses can be too superficial or imprecise when addressing highly technical or niche topics. This limits their usefulness in research, where deep expertise and accurate, detailed information are essential.</p><h2 id="offline-software-package" tabindex="-1">Offline Software Package <a class="header-anchor" href="#offline-software-package" aria-label="Permalink to &quot;Offline Software Package&quot;">​</a></h2><p>We took these situations into account and developed an offline package designed to meet the unique needs of researchers concerned about data privacy and security. This package empowers users to create their own private knowledge bases tailored to their specific requirements. With this tool, users have complete control over the content, allowing them to curate and manage information without the fear of data leakage or unauthorized access. Furthermore, the package is built on open-source software, enabling users to modify and customize it according to their individual needs. This flexibility ensures that researchers can adapt the tool to their workflows, enhancing both productivity and confidence in their data management practices.</p><div class="tip custom-block"><p class="custom-block-title">TIP</p><p>This document focuses on the introduction and use of local software packages developed by our team.</p></div>',19)]))}const m=t(n,[["render",r]]);export{u as __pageData,m as default};
