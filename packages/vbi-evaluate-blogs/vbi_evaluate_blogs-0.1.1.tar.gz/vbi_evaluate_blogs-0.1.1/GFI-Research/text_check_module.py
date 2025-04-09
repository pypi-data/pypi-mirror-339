from langchain_openai import AzureChatOpenAI

def check_references(llm: AzureChatOpenAI, text: str) -> str:
    return ""

def check_article_structure(llm: AzureChatOpenAI, text: str) -> str:  
    """Check the structure of the article based on predefined rules."""  

    prompt = f"""
    <EvaluationRequest>
        <Role>
            You are a <strong>web content evaluation expert</strong> with professional experience in optimizing article structures.
        </Role>

        <Mission>
            <Overview>
                Your mission is to <strong>check and evaluate the structure of the article</strong> based on technical and academic criteria.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Check the main components</Title>
                    <Details>
                        <Point>Title: Is it appropriately long and does it accurately reflect the content of the article?</Point>
                        <Point>Summary (Key Insights): Does it briefly describe the problem, insights, and results of the article?</Point>
                        <Point>Introduction & Objective: Does it clearly state the research problem and objectives?</Point>
                        <Point>Detailed Presentation: Does it delve into the aspects of the problem?</Point>
                        <Point>Conclusion: Does it explain, discuss, and highlight the significance of the results?</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Analyze detailed aspects</Title>
                    <Details>
                        <Point>Technology/Model Analysis: Is it clearly presented?</Point>
                        <Point>Position and Competitors: Is it comprehensively evaluated?</Point>
                        <Point>Applications: Are real-world applications clearly stated?</Point>
                        <Point>Financial/Parameter/Valuation Analysis: Are supporting data provided?</Point>
                        <Point>Investment Perspective: Are reasonable viewpoints presented?</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Identify issues and suggest improvements</Title>
                    <Details>
                        <Point>If any component is missing, list specific errors.</Point>
                        <Point>If the structure is illogical, suggest a reorganization.</Point>
                        <Point>Provide suggestions to optimize each section for higher quality.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <OutputFormat>
            <Field>Respond in Markdown format.</Field>
            <Field>Respond in English. Only quoted content should remain in Vietnamese.</Field>
            <Section title="Overview">
                <Field>Overall evaluation of the structure: ...</Field>
                <Field>Score: x/10</Field>
            </Section>

            <Section title="Detailed Evaluation">
                <IssueStructure>
                    <CriterionTitle>Title</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Summary (Key Insights)</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Introduction & Objective</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Detailed Presentation</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Conclusion</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
            </Section>>
        </OutputFormat>

        <Content>
            {text}
        </Content>
    </EvaluationRequest>
    """
    # Invoke the LLM with the evaluation criteria and content
    response = llm.invoke(prompt)
    # with open("output/check_article_struture.txt", "w", encoding="utf-8") as f:
    #     f.write(response.content)
    return response.content

def check_content(llm: AzureChatOpenAI, text: str) -> str:
    """Evaluate the content of each section of the article based on predefined rules."""
    
    prompt = f"""
    <EvaluationRequest>
        <Role>
            You are a <strong>content evaluation expert</strong> with in-depth analysis experience and expertise in assessing article quality.
        </Role>

        <Mission>
            <Overview>
                Your mission is to <strong>evaluate the content of each section of the article in GREAT DETAIL</strong> based on predefined criteria, ensuring the article achieves the highest quality.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Key Insights</Title>
                    <Details>
                        <Point>Summarize the main points of the article briefly.</Point>
                        <Point>Identify the main issue the article will analyze.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Overview of the Research Topic</Title>
                    <Details>
                        <Point>Introduce the topic or project, including its development history and current status.</Point>
                        <Point>Highlight the problem or challenge to be addressed.</Point>
                        <Point>Clearly define the objectives of the article.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Detailed Analysis</Title>
                    <Details>
                        <Point>Use market data and case studies to support arguments. Ensure the analysis is backed by specific examples and real-world applications.</Point>
                        <Point>Only use data from reputable sources, ensuring high accuracy and reliability. Data must be filtered, analyzed, and processed objectively.</Point>
                        <Point>Avoid imposing subjective opinions; respect the objectivity of events and data.</Point>
                    </Details>
                    <SubInstruction>
                        <Title>3.1 Technology Analysis</Title>
                        <Details>
                            <Point>Explain the foundational technology: Analyze the core technology of the project, reasons for its development, and technical highlights.</Point>
                            <Point>Compare with other technologies: Highlight strengths and weaknesses compared to similar solutions in the market.</Point>
                            <Point>Analyze performance and scalability: Evaluate processing capabilities, performance, scalability potential, and potential issues.</Point>
                        </Details>
                    </SubInstruction>

                    <SubInstruction>
                        <Title>3.2 Position and Competitors</Title>
                        <Details>
                            <Point>Compare with competitors: Analyze the project's position in the market, using data to substantiate.</Point>
                            <Point>Evaluate market potential and growth opportunities: Analyze the project's future opportunities and challenges.</Point>
                        </Details>
                    </SubInstruction>

                    <SubInstruction>
                        <Title>3.3 Applications</Title>
                        <Details>
                            <Point>Provide specific use cases: Examples of how the project or technology is applied in practice (DeFi, NFT, blockchain infrastructure, etc.).</Point>
                            <Point>Analyze impact on users and the market: Draw lessons or predictions for the future.</Point>
                        </Details>
                    </SubInstruction>

                    <SubInstruction>
                        <Title>3.4 Financial/Parameter/Valuation Analysis</Title>
                        <Details>
                            <Point>Financial analysis: Evaluate financial indicators such as trading volume, locked value (TVL), and financial performance.</Point>
                            <Point>Valuation and growth potential: Provide valuation scenarios based on market and intrinsic factors.</Point>
                        </Details>
                    </SubInstruction>

                    <SubInstruction>
                        <Title>3.5 Investment Perspective</Title>
                        <Details>
                            <Point>Provide strategies and investment methods: Evaluate the feasibility and effectiveness of each method.</Point>
                            <Point>Analyze risks and opportunities: Suggest measures to mitigate risks.</Point>
                        </Details>
                    </SubInstruction>
                </Instruction>

                <Instruction>
                    <Title>4. Conclusion</Title>
                    <Details>
                        <Point>Summarize the main points discussed.</Point>
                        <Point>Highlight new narratives or development potential of the project.</Point>
                        <Point>Provide a call to action or suggestions for readers.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <OutputFormat>
            <Field>Respond in Markdown format.</Field>
            <Field>Respond in English. Only quoted content should remain in Vietnamese.</Field>
            <Section title="Overview">
                <Field>Overall evaluation of the content: ...</Field>
                <Field>Score: x/10</Field>
            </Section>

            <Section title="Detailed Evaluation">
                <IssueStructure>
                    <CriterionTitle>Key Insights</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Overview of the Topic</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Detailed Analysis</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Conclusion</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
            </Section>
        </OutputFormat>

        <Content>
            {text}
        </Content>
    </EvaluationRequest>
    """
    # Invoke the LLM with the evaluation criteria and content
    response = llm.invoke(prompt)
    # with open("output/check_content.txt", "w", encoding="utf-8") as f:
    #     f.write(response.content)
    return response.content

def check_grammar_error(llm: AzureChatOpenAI, text: str) -> str:
    """Check grammar, spelling, style, and content requirements related to web3, blockchain, crypto, and smart-contract."""
    
    prompt = f"""
    <EvaluationRequest>
        <Role>
            You are a <strong>language expert</strong> with in-depth evaluation experience in the field of <strong>web3, blockchain, crypto, and smart-contract</strong>.
        </Role>

        <Mission>
            <Overview>
                Your mission is to <strong>check and evaluate the style, grammar, and spelling</strong> of the article, ensuring the content meets the highest standards of quality and relevance to the specialized field.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Check grammar and spelling</Title>
                    <Details>
                        <Point>Identify grammatical, spelling, and punctuation errors.</Point>
                        <Point>Ensure sentences are clear, grammatically correct, and unambiguous.</Point>
                        <Point>Quote the erroneous sentences in Vietnamese and suggest corrections in English.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Check style and length</Title>
                    <Details>
                        <Point>Ensure professional style suitable for the field of web3, blockchain, crypto, and smart-contract.</Point>
                        <Point>Check the article length, ensuring a minimum of 2500 words.</Point>
                        <Point>Identify overly long or short paragraphs and suggest ways to split or expand content.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Check for word repetition</Title>
                    <Details>
                        <Point>Identify unnecessary word repetition (except for important keywords).</Point>
                        <Point>Suggest synonyms or alternative expressions to avoid repetition.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>4. Evaluate coherence and linkage</Title>
                    <Details>
                        <Point>Ensure paragraphs have logical connections, not disjointed.</Point>
                        <Point>Check if the main ideas are clearly and coherently presented.</Point>
                        <Point>Suggest improvements if needed.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>5. Suggest improvements</Title>
                    <Details>
                        <Point>If the article can be improved in style, grammar, or presentation, provide specific suggestions.</Point>
                        <Point>Ensure the article is easy to read and understand while maintaining high professionalism.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <OutputFormat>
            <Field>Respond in Markdown format.</Field>
            <Field>Respond in English. Only quoted content should remain in Vietnamese.</Field>
            <Section title="Overview">
                <Field>Overall evaluation of grammar, spelling, and style: ...</Field>
                <Field>Score: x/10</Field>
            </Section>

            <Section title="Detailed Evaluation">
                <IssueStructure>
                    <CriterionTitle>Grammar and Spelling</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Style and Length</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Word Repetition</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Coherence and Linkage</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
            </Section>
        </OutputFormat>

        <Content>
            {text}
        </Content>
    </EvaluationRequest>
    """
    # Invoke the LLM with the evaluation criteria and content
    response = llm.invoke(prompt)
    # with open("output/check_grammar_error.txt", "w", encoding="utf-8") as f:
    #     f.write(response.content)
    return response.content

def check_keyword_distribution(llm: AzureChatOpenAI, text: str) -> str:  
    """Check keyword distribution in the article."""  
    prompt = f"""
    <EvaluationRequest>
        <Role>
            You are a <strong>SEO expert</strong> with experience in optimizing content for high performance on search engines.
        </Role>

        <Mission>
            <Overview>
                Your mission is to <strong>check and evaluate keyword distribution</strong> in the article, ensuring SEO optimization without keyword stuffing.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Identify and analyze main keywords</Title>
                    <Details>
                        <Point>Do main keywords appear in the title, H1 tag, and meta description?</Point>
                        <Point>Do main keywords appear in the first 100 words of the article?</Point>
                        <Point>Are main keywords used naturally, not forced?</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Evaluate keyword distribution in content</Title>
                    <Details>
                        <Point>Is the main keyword density within 1-2% of the total word count?</Point>
                        <Point>Are variations (LSI keywords) and synonyms used instead of repeating the main keywords excessively?</Point>
                        <Point>Do H2 and H3 tags contain secondary keywords appropriately?</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Identify issues and suggest improvements</Title>
                    <Details>
                        <Point>If main keywords are overused (above 2.5%), point out specific areas for adjustment.</Point>
                        <Point>If the article lacks keywords or keywords are distributed inappropriately, suggest improvements.</Point>
                        <Point>Recommend using synonyms and keyword variations to avoid excessive repetition.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <OutputFormat>
            <Section title="Overview">
                <Field>Respond in Markdown format.</Field>
                <Field>Overall evaluation of keyword distribution: ...</Field>
                <Field>Score: x/10</Field>
            </Section>

            <Section title="Detailed Evaluation">
                <IssueStructure>
                    <CriterionTitle>Appearance in Title, H1, Meta</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Appearance in First 100 Words</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Keyword Density</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Keyword Stuffing</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Keyword Variations & LSI</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
            </Section>
        </OutputFormat>

        <Content>
            {text}
        </Content>
    </EvaluationRequest>
    """

    # Invoke the LLM with the evaluation criteria and content
    response = llm.invoke(prompt)
    return response.content

def evaluate_readability(llm: AzureChatOpenAI, text: str) -> str:  
    """Evaluate the readability and style of the article."""  
    prompt = f"""
    <EvaluationRequest>
        <Role>
            You are a <strong>language and content optimization expert</strong> with experience in evaluating readability and style of articles.
        </Role>

        <Mission>
            <Overview>
                Your mission is to <strong>evaluate the readability and style of the article</strong>, ensuring the content is clear, coherent, easy to understand, yet professional and suitable for the target audience.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Evaluate readability</Title>
                    <Details>
                        <Point>Calculate readability score based on Flesch-Kincaid or equivalent index.</Point>
                        <Point>Are sentences too long or complex?</Point>
                        <Point>Is the language simple and easy to understand or overly academic?</Point>
                        <Point>Is paragraph length reasonable? (Too long can be hard to read)</Point>
                        <Point>Are lists and bullet points used to enhance content absorption?</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Evaluate style</Title>
                    <Details>
                        <Point>Is the style suitable for the target audience? (Highly technical, general, marketing...)</Point>
                        <Point>Is the language accurate, objective, avoiding emotional bias?</Point>
                        <Point>Are sentences clear, not ambiguous or misleading?</Point>
                        <Point>Is the tone consistent? (Avoid mixing formal and casual)</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Suggest improvements</Title>
                    <Details>
                        <Point>If sentences are too long or complex, suggest rewriting them more concisely.</Point>
                        <Point>If paragraphs are too dense, suggest splitting them into reasonable sections.</Point>
                        <Point>If the article lacks lists or specific examples, suggest ways to add them.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <OutputFormat>
            <Section title="Overview">
                <Field>Respond in Markdown format.</Field>
                <Field>Overall readability evaluation: ...</Field>
                <Field>Readability score (based on Flesch-Kincaid or equivalent): x/100</Field>
                <Field>General comments on style: ...</Field>
            </Section>

            <Section title="Detailed Evaluation">
                <IssueStructure>
                    <CriterionTitle>Sentence Length</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Paragraph Length</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Language & Understandability</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Style & Tone</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
            </Section>
        </OutputFormat>

        <Content>
            {text}
        </Content>
    </EvaluationRequest>
    """

    # Invoke the LLM with the evaluation criteria and content
    response = llm.invoke(prompt)
    return response.content

def check_uniqueness(llm: AzureChatOpenAI, text: str) -> str:  
    """Check the uniqueness of the content."""  
    prompt = f"""
    <EvaluationRequest>
        <Role>
            You are a <strong>plagiarism detection and uniqueness evaluation expert</strong> for article content.
        </Role>

        <Mission>
            <Overview>
                Your mission is to <strong>check the level of content duplication</strong>, ensuring the article is unique, not copied or overly borrowed from other sources without creativity or added value.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Check for content duplication</Title>
                    <Details>
                        <Point>Identify sections that may have been copied from other sources.</Point>
                        <Point>Compare with popular texts, public documents, and web articles.</Point>
                        <Point>If duplication is found, quote the original text and determine the level of duplication.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Evaluate uniqueness</Title>
                    <Details>
                        <Point>Does the article provide unique perspectives, analyses, or expressions?</Point>
                        <Point>Is it creative or merely repeating information from other sources?</Point>
                        <Point>If the article cites materials, are sources clearly stated?</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Suggest edits if necessary</Title>
                    <Details>
                        <Point>If a section can be rewritten to be more distinctive, suggest alternative phrasing.</Point>
                        <Point>If citation sources need to be added, point out specific locations.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <OutputFormat>
            <Section title="Overview">
                <Field>Respond in Markdown format.</Field>
                <Field>Uniqueness level: x%</Field>
                <Field>General comments: ...</Field>
            </Section>

            <Section title="Detailed Duplication Findings">
                <IssueStructure>
                    <OriginalText>"..."</OriginalText>
                    <Source>Found duplicate with: [URL/Source]</Source>
                    <SimilarityLevel>x%</SimilarityLevel>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <!-- Repeat if multiple duplicate sections -->
            </Section>

            <Section title="Improvement Suggestions">
                <FixStructure>
                    <OriginalText>"..."</OriginalText>
                    <SuggestedRewrite>...</SuggestedRewrite>
                    <Reason>...</Reason>
                </FixStructure>
                <!-- Repeat if necessary -->
            </Section>
        </OutputFormat>

        <Content>
            {text}
        </Content>
    </EvaluationRequest>
    """

    # Invoke the LLM with the evaluation criteria and content
    response = llm.invoke(prompt)
    return response.content

def check_internal_external_links(llm: AzureChatOpenAI, text: str) -> str:  
    """Check internal and external links (internal & backlink)."""  
    pass  

def evaluate_research_depth(llm: AzureChatOpenAI, text: str) -> str:  
    """Evaluate the depth of research and level of evidence."""  
    prompt = f"""
    <EvaluationRequest>
        <Role>
            You are a <strong>content evaluation expert</strong> with high standards, requiring articles to have <strong>deep research</strong> and <strong>convincing evidence</strong>.
        </Role>

        <Mission>
            <Overview>
                You need to <strong>evaluate the depth of research</strong> of the article below, considering the use of references, data, and evidence supporting arguments.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Determine the level of research</Title>
                    <Details>
                        <Point>Does the article <strong>use reliable references?</strong> (credible sources such as scientific studies, reports, books, official articles).</Point>
                        <Point>If no references are provided, <strong>point out weaknesses</strong> and suggest suitable sources.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Evaluate the level of evidence</Title>
                    <Details>
                        <Point>Does the article **use specific data and statistics** to support arguments?</Point>
                        <Point>If data is provided, **check if the source is credible** (avoid Wikipedia, personal blogs, unclear sources).</Point>
                        <Point>If the article only provides **general arguments without evidence**, point out weaknesses and suggest improvements.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Evaluate comparisons and multi-dimensional perspectives</Title>
                    <Details>
                        <Point>Does the article consider **different perspectives** on the issue?</Point>
                        <Point>If the article only provides one-sided views, suggest adding other perspectives to increase objectivity.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>4. Check the level of in-depth analysis</Title>
                    <Details>
                        <Point>Does the article delve into the issue, providing detailed analysis?</Point>
                        <Point>If it only scratches the surface, suggest ways to delve deeper into key points.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <Criteria>
            <Criterion>
                <Title>1. Research & References (10 points)</Title>
                <Checklist>
                    <Item>Are reliable references used?</Item>
                    <Item>Avoid Wikipedia, personal blogs?</Item>
                </Checklist>
            </Criterion>

            <Criterion>
                <Title>2. Level of Evidence (10 points)</Title>
                <Checklist>
                    <Item>Are data and statistics used?</Item>
                    <Item>Are data sources credible?</Item>
                </Checklist>
            </Criterion>

            <Criterion>
                <Title>3. Comparisons and Multi-Dimensional Perspectives (10 points)</Title>
                <Checklist>
                    <Item>Are different perspectives considered?</Item>
                    <Item>Are differences between perspectives analyzed?</Item>
                </Checklist>
            </Criterion>

            <Criterion>
                <Title>4. Depth of Analysis (10 points)</Title>
                <Checklist>
                    <Item>Does the article delve into the issue?</Item>
                    <Item>Or does it only scratch the surface?</Item>
                </Checklist>
            </Criterion>
        </Criteria>

        <OutputFormat>
            <Section title="Overview">
                <Field>Respond in Markdown format.</Field>
                <Field>Total score: .../40</Field>
                <Field>General comments: ...</Field>
            </Section>

            <Section title="Detailed Evaluation of Each Criterion">
                <CriterionEvaluation>
                    <CriterionTitle>1. Research & References: x/10</CriterionTitle>
                    <Pros>✅ Strengths: ...</Pros>
                    <Cons>❌ Weaknesses: ...</Cons>
                    <Suggestions>💡 Suggestions: ...</Suggestions>
                </CriterionEvaluation>

                <CriterionEvaluation>
                    <CriterionTitle>2. Level of Evidence: x/10</CriterionTitle>
                    <Pros>✅ Strengths: ...</Pros>
                    <Cons>❌ Weaknesses: ...</Cons>
                    <Suggestions>💡 Suggestions: ...</Suggestions>
                </CriterionEvaluation>

                <CriterionEvaluation>
                    <CriterionTitle>3. Comparisons and Multi-Dimensional Perspectives: x/10</CriterionTitle>
                    <Pros>✅ Strengths: ...</Pros>
                    <Cons>❌ Weaknesses: ...</Cons>
                    <Suggestions>💡 Suggestions: ...</Suggestions>
                </CriterionEvaluation>

                <CriterionEvaluation>
                    <CriterionTitle>4. Depth of Analysis: x/10</CriterionTitle>
                    <Pros>✅ Strengths: ...</Pros>
                    <Cons>❌ Weaknesses: ...</Cons>
                    <Suggestions>💡 Suggestions: ...</Suggestions>
                </CriterionEvaluation>
            </Section>
        </OutputFormat>

        <Content>
            --- START OF ARTICLE TO BE EVALUATED ---
            {text}
            --- END OF ARTICLE ---
        </Content>
    </EvaluationRequest>
    """
    
    # Invoke the LLM with the evaluation criteria and content
    response = llm.invoke(prompt)
    return response.content

def check_logic_and_objectivity(llm: AzureChatOpenAI, text: str) -> str:  
    """Check the logic and objectivity of the article."""  
    pass  

def check_grammar_and_spelling(llm: AzureChatOpenAI, text: str) -> str:  
    """Check grammar and spelling errors."""  
    pass  

def check_conclusion_and_cta(llm: AzureChatOpenAI, text: str) -> str:  
    """Check the conclusion and call-to-action (CTA)."""  
    pass  

# Function to evaluate the content of a PDF based on predefined criteria using an LLM
def ContentCheck(llm: AzureChatOpenAI, text: str) -> str:
    """
    Evaluate the content of a PDF based on predefined criteria using the provided LLM.

    Args:
        content (str): The extracted text content from the PDF.
        llm (AzureChatOpenAI): The initialized AzureChatOpenAI instance.

    Returns:
        str: The evaluation result.
    """
    require = f"""
    <EvaluationRequest>
        <Role>
            You are a <strong>strict, meticulous, and highly specialized content evaluation expert</strong> in the field of <strong>blockchain, crypto, smart contract</strong>.
        </Role>

        <Mission>
            <Overview>
                You need to <strong>analyze, score, and provide detailed feedback</strong> on the article content below based on academic criteria.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Score each criterion on a scale of 10, with a maximum total score of 100.</Title>
                    <Details>
                        <Point>If scoring below 8, clearly state the <strong>reason for the deduction</strong>.</Point>
                        <Point>If the content is good but can be upgraded, <strong>provide suggestions to make it excellent</strong>.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Identify specific issues in the article:</Title>
                    <Details>
                        <Point>Sentences that are <strong>inaccurate, emotional, vague, or lack evidence</strong>.</Point>
                        <Point>**Always check the surrounding context** (preceding and following paragraphs) before judging a sentence as vague or lacking information.</Point>
                        <Point>Paragraphs that are <strong>smooth but superficial, lack depth of analysis, or lack logical connections</strong>.</Point>
                        <Point>Content that is <strong>repetitive, redundant, or misleading</strong>.</Point>
                    </Details>
                    <ErrorHandling>
                        <Point>Quote the problematic paragraph verbatim (if possible).</Point>
                        <Point>Do not evaluate a sentence as “lacking evidence” or “vague” if the evidence is in the adjacent preceding or following paragraph.</Point>
                        <Point>If in doubt, quote additional preceding/following paragraphs to check the context.</Point>
                        <Point>Explain why the paragraph is problematic.</Point>
                        <Point>Suggest rewriting or reasonable adjustments.</Point>
                    </ErrorHandling>
                </Instruction>

                <Instruction>
                    <Title>3. Present results in Markdown</Title>
                    <Details>
                        <Point>Use symbols:
                            <Symbols>
                                <Symbol>✅ Strengths</Symbol>
                                <Symbol>❌ Weaknesses</Symbol>
                                <Symbol>💡 Suggestions</Symbol>
                            </Symbols>
                        </Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>4. Check grammar and spelling</Title>
                    <Details>
                        <Point>Detect and list spelling, grammar, word usage errors, repetition, or inappropriate punctuation.</Point>
                        <Point>If errors are found, quote the erroneous sentences and suggest correct phrasing.</Point>
                        <Point>If the article is well-written, still point out some sections that could be rewritten for smoother flow.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <Criteria>
            <Criterion>
                <Title>1. Clear Content and Objectives (10 points)</Title>
                <Checklist>
                    <Item>Are objectives clear?</Item>
                    <Item>Is the target audience identified?</Item>
                    <Item>Is the issue practical and provides tangible value?</Item>
                </Checklist>
            </Criterion>

            <Criterion>
                <Title>2. Depth of Research and References (10 points)</Title>
                <Checklist>
                    <Item>Are reliable sources cited?</Item>
                    <Item>Are opposing viewpoints used?</Item>
                    <Item>Avoid Wikipedia, personal blogs?</Item>
                </Checklist>
            </Criterion>

            <Criterion>
                <Title>3. Logical Structure (10 points)</Title>
                <Checklist>
                    <Item>Are main sections like Title, Summary, Introduction, Analysis, Conclusion present?</Item>
                    <Item>Are sections logically connected and coherently presented?</Item>
                </Checklist>
            </Criterion>

            <Criterion>
                <Title>4. In-Depth Analysis and Supporting Data (20 points)</Title>
                <Checklist>
                    <Item>Are specific data provided?</Item>
                    <Item>Is the analysis in-depth?</Item>
                    <Item>Are comparisons with competitors made?</Item>
                </Checklist>
            </Criterion>

            <Criterion>
                <Title>5. Objectivity and Reasonableness (10 points)</Title>
                <Checklist>
                    <Item>Avoid bias, emotionality?</Item>
                    <Item>Neutral evaluation based on facts?</Item>
                </Checklist>
            </Criterion>

            <Criterion>
                <Title>6. Style and Presentation (10 points)</Title>
                <Checklist>
                    <Item>Professional style, easy to understand?</Item>
                    <Item>Clear headings, bullet points?</Item>
                    <Item>Explain technical terms?</Item>
                    <Item>Length ≥ 2500 words?</Item>
                </Checklist>
            </Criterion>

            <Criterion>
                <Title>7. Evaluation of Results and Call to Action (10 points)</Title>
                <Checklist>
                    <Item>Does the conclusion summarize key points?</Item>
                    <Item>Does it highlight potential, risks, next steps?</Item>
                </Checklist>
            </Criterion>

            <Criterion>
                <Title>8. Language and Spelling (10 points)</Title>
                <Checklist>
                    <Item>Correct spelling, no typos?</Item>
                    <Item>Clear sentences, grammatically correct?</Item>
                    <Item>Avoid repetition, incorrect word usage, or inappropriate context?</Item>
                    <Item>Reasonable punctuation, easy to read?</Item>
                </Checklist>
            </Criterion>
        </Criteria>

        <OutputFormat>
            <Section title="Overview">
                <Field>Respond in Markdown format.</Field>
                <Field>Total score: .../100</Field>
                <Field>General comments: ...</Field>
            </Section>

            <Section title="Detailed Evaluation of Each Criterion">
                <CriterionEvaluation>
                    <CriterionTitle>1. Clear Content and Objectives: x/10</CriterionTitle>
                    <Pros>✅ Strengths: ...</Pros>
                    <Cons>❌ Weaknesses: ...</Cons>
                    <Suggestions>💡 Suggestions: ...</Suggestions>
                </CriterionEvaluation>
                <!-- Repeat for other criteria -->
            </Section>

            <Section title="Specific Areas for Improvement">
                <IssueStructure>
                    <OriginalText>"This project is extremely promising because everyone mentions it"</OriginalText>
                    <Problem>Lacks evidence, emotional</Problem>
                    <FixSuggestion>Provide specific data, e.g., TVL increase, active users, etc., to substantiate</FixSuggestion>
                </IssueStructure>
                <!-- Repeat if necessary -->
            </Section>

            <Section title="Grammar and Spelling Errors">
                <IssueStructure>
                    <OriginalText>"However, the project has a small but important issue."</OriginalText>
                    <Problem>Spelling error: "important" → "important"</Problem>
                    <FixSuggestion>Rewrite: "However, the project has a small but important issue."</FixSuggestion>
                </IssueStructure>
                <!-- Repeat if necessary -->
            </Section>

        </OutputFormat>

        <Note>
            <Point>Do not include sample examples.</Point>
            <Point>If the article does not address a criterion, you may skip it but must state the reason.</Point>
            <Point>Avoid evaluating sentences in isolation. A sentence may be an introduction to the explanation that follows.</Point>
            <Point>Provide honest evaluations, no flattery. Praise appropriately if the article is good, and provide specific feedback if it is poor.</Point>
            <Point>If the article is good but not excellent, suggest ways to help it <strong>exceed standards</strong>.</Point>
        </Note>

        <Content>
        --- START OF ARTICLE TO BE EVALUATED ---
        {text}
        --- END OF ARTICLE ---
        </Content>
    </EvaluationRequest>
    """

    # Invoke the LLM with the evaluation criteria and content
    response = llm.invoke(require)
    return response.content

def text_check(llm: AzureChatOpenAI, text: str) -> str:
    """Comprehensive content evaluation of the article"""

    check_article_structure_result=check_article_structure(llm,text)
    check_content_result=check_content(llm,text)
    check_grammar_error_result=check_grammar_error(llm,text)

    sumarize_result = f"""
    Results of structure evaluation based on article requirements:
    {check_article_structure_result}

    Results of content evaluation based on article requirements:
    {check_content_result}

    Results of grammar, spelling, style, and length evaluation:
    {check_grammar_error_result}
    """

    # with open("output/check_text.txt", "w", encoding="utf-8") as f:
    #     f.write(sumarize_result)
    print(sumarize_result)
    return sumarize_result

if __name__ == "__main__":
    import os
    import extract_module
    from langchain_openai import AzureChatOpenAI
    from dotenv import load_dotenv
    # Load environment variables from .env file
    load_dotenv()

    # Initialize Azure OpenAI API with credentials and configuration
    llm = AzureChatOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        model="o3-mini",
        api_version="2024-12-01-preview",
        # temperature=0.7,
        # max_tokens=16000
    )

    # Path to the PDF file to be evaluated
    pdf_path = 'data/tc13.pdf'

    # Extract text content from the PDF
    text = extract_module.extract_text(pdf_path)

    # check_article_structure(llm, text)

    # check_content(llm,text)

    # check_grammar_error(llm,text)

    text_check(llm,text)