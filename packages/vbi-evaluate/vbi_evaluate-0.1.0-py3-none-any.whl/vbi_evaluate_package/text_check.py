def check_references(llm,text):

    return

def check_article_structure(llm, text):  
    """Kiểm tra cấu trúc bài viết theo các quy tắc đã định nghĩa."""  

    prompt = f"""
    <EvaluationRequest>
        <Role>
            Bạn là một <strong>chuyên gia đánh giá nội dung web</strong>, có kinh nghiệm tối ưu hóa cấu trúc bài viết chuyên nghiệp.
        </Role>

        <Mission>
            <Overview>
                Nhiệm vụ của bạn là <strong>kiểm tra và đánh giá cấu trúc bài viết</strong> dựa trên các tiêu chí kỹ thuật và học thuật.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Kiểm tra các thành phần chính</Title>
                    <Details>
                        <Point>Tiêu đề (Title): Có độ dài vừa đủ và phản ánh đúng nội dung bài viết không?</Point>
                        <Point>Tóm tắt (Key Insights): Có mô tả vắn tắt vấn đề, insights và kết quả bài viết không?</Point>
                        <Point>Đặt vấn đề và Mục tiêu (Introduction & Objective): Có nêu rõ vấn đề nghiên cứu và mục tiêu không?</Point>
                        <Point>Trình bày chi tiết: Có đào sâu các khía cạnh của vấn đề không?</Point>
                        <Point>Kết luận: Có giải thích, bàn luận và nêu ý nghĩa của kết quả không?</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Phân tích chi tiết các khía cạnh</Title>
                    <Details>
                        <Point>Phân tích công nghệ/mô hình: Có trình bày rõ ràng không?</Point>
                        <Point>Vị thế và đối thủ cạnh tranh: Có đánh giá đầy đủ không?</Point>
                        <Point>Ứng dụng: Có nêu rõ các ứng dụng thực tế không?</Point>
                        <Point>Phân tích tài chính/thông số/định giá: Có cung cấp số liệu chứng minh không?</Point>
                        <Point>Cách tiếp cận từ góc nhìn đầu tư: Có đưa ra quan điểm hợp lý không?</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Phát hiện và đề xuất cải thiện</Title>
                    <Details>
                        <Point>Nếu thiếu bất kỳ thành phần nào, hãy liệt kê các lỗi cụ thể.</Point>
                        <Point>Nếu cấu trúc không hợp lý, đề xuất cách sắp xếp lại.</Point>
                        <Point>Gợi ý cách tối ưu từng phần để bài viết đạt chất lượng cao hơn.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <OutputFormat>
            <Field>Trả lời bằng định dạng Markdown.</Field>
            <Field>Chỉ trả về đúng nội dung cần thiết không cần ký hiệu gì thêm.</Field>
            <Field>Dịch 2 từ Analysis và FixSuggestion sang tiếng Việt</Field>
            <Section title="Tổng Quan">
                <Field>Đánh giá tổng thể về cấu trúc: ...</Field>
                <Field>Điểm đánh giá: x/10</Field>
            </Section>

            <Section title="Chi Tiết Đánh Giá">
                <IssueStructure>
                    <CriterionTitle>Tiêu đề (Title)</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Tóm tắt (Key Insights)</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Đặt vấn đề và Mục tiêu (Introduction & Objective)</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Trình bày chi tiết</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Kết luận</CriterionTitle>
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
    with open("output/check_article_struture.txt", "w", encoding="utf-8") as f:
        f.write(response.content)
    return response.content

def check_content(llm, text):
    """Đánh giá nội dung từng phần của bài viết theo các quy tắc đã định nghĩa."""
    
    prompt = f"""
    <EvaluationRequest>
        <Role>
            Bạn là một <strong>chuyên gia đánh giá nội dung</strong> với kinh nghiệm phân tích chuyên sâu và đánh giá chất lượng bài viết.
        </Role>

        <Mission>
            <Overview>
                Nhiệm vụ của bạn là <strong>đánh giá <Strong>THẬT CHI TIẾT</Strong> nội dung từng phần của bài viết</strong> dựa trên các tiêu chí đã định nghĩa, đảm bảo bài viết đạt chất lượng cao nhất.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Key Insights</Title>
                    <Details>
                        <Point>Tóm tắt ngắn gọn các điểm chính của bài viết.</Point>
                        <Point>Định vị vấn đề chính mà bài viết sẽ phân tích.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Tổng quan về chủ đề nghiên cứu</Title>
                    <Details>
                        <Point>Giới thiệu về chủ đề hoặc dự án, bao gồm lịch sử phát triển và tình trạng hiện tại.</Point>
                        <Point>Đặt ra vấn đề hoặc thách thức cần giải quyết.</Point>
                        <Point>Xác định rõ mục tiêu của bài viết.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Phân tích chi tiết</Title>
                    <Details>
                        <Point>Sử dụng dữ liệu thị trường và nghiên cứu tình huống để hỗ trợ các lập luận. Đảm bảo bài phân tích được hỗ trợ bởi các ví dụ cụ thể và ứng dụng thực tế.</Point>
                        <Point>Chỉ sử dụng dữ liệu từ các nguồn uy tín, đảm bảo độ chính xác và tin cậy cao. Các dữ kiện cần được sàng lọc, phân tích và xử lý khách quan.</Point>
                        <Point>Không được áp đặt ý kiến chủ quan, phải tôn trọng tính khách quan của sự kiện và số liệu.</Point>
                    </Details>
                    <SubInstruction>
                        <Title>3.1 Phân tích về công nghệ</Title>
                        <Details>
                            <Point>Giải thích công nghệ nền tảng: Phân tích công nghệ cốt lõi của dự án, lý do xây dựng và các điểm nổi bật kỹ thuật.</Point>
                            <Point>So sánh với các công nghệ khác: Nhấn mạnh điểm mạnh và điểm yếu so với các giải pháp tương tự trên thị trường.</Point>
                            <Point>Phân tích hiệu suất và khả năng mở rộng: Đánh giá khả năng xử lý, hiệu suất, tiềm năng mở rộng, và các vấn đề tiềm ẩn.</Point>
                        </Details>
                    </SubInstruction>

                    <SubInstruction>
                        <Title>3.2 Vị thế và đối thủ cạnh tranh</Title>
                        <Details>
                            <Point>So sánh với đối thủ cạnh tranh: Phân tích vị thế của dự án trong thị trường, sử dụng số liệu để chứng minh.</Point>
                            <Point>Đánh giá thị trường và tiềm năng tăng trưởng: Phân tích cơ hội và thách thức của dự án trong tương lai.</Point>
                        </Details>
                    </SubInstruction>

                    <SubInstruction>
                        <Title>3.3 Ứng dụng</Title>
                        <Details>
                            <Point>Đưa ra các trường hợp sử dụng cụ thể: Ví dụ về cách dự án hoặc công nghệ được áp dụng trong thực tế (DeFi, NFT, cơ sở hạ tầng blockchain, v.v.).</Point>
                            <Point>Phân tích tác động đến người dùng và thị trường: Rút ra bài học hoặc dự đoán cho tương lai.</Point>
                        </Details>
                    </SubInstruction>

                    <SubInstruction>
                        <Title>3.4 Phân tích thông số/tài chính/định giá</Title>
                        <Details>
                            <Point>Phân tích tài chính: Đánh giá các chỉ số tài chính như khối lượng giao dịch, giá trị bị khóa (TVL), và hiệu suất tài chính.</Point>
                            <Point>Định giá và tiềm năng tăng giá: Đưa ra các kịch bản định giá dựa trên yếu tố thị trường và nội tại.</Point>
                        </Details>
                    </SubInstruction>

                    <SubInstruction>
                        <Title>3.5 Cách tiếp cận theo góc nhìn đầu tư</Title>
                        <Details>
                            <Point>Đưa ra chiến lược và phương pháp đầu tư: Đánh giá tính khả thi và hiệu quả của từng phương pháp.</Point>
                            <Point>Phân tích rủi ro và cơ hội: Đề xuất các biện pháp giảm thiểu rủi ro.</Point>
                        </Details>
                    </SubInstruction>
                </Instruction>

                

                <Instruction>
                    <Title>4. Kết luận</Title>
                    <Details>
                        <Point>Tóm tắt các điểm chính đã thảo luận.</Point>
                        <Point>Nhấn mạnh narrative mới hoặc tiềm năng phát triển của dự án.</Point>
                        <Point>Đưa ra kêu gọi hành động hoặc đề xuất cho người đọc.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <OutputFormat>
            <Field>Trả lời bằng định dạng Markdown.</Field>
            <Field>Chỉ trả về đúng nội dung cần thiết không cần ký hiệu gì thêm.</Field>
            <Field>Dịch 2 từ Analysis và FixSuggestion sang tiếng Việt</Field>
            <Section title="Tổng Quan">
                <Field>Đánh giá tổng thể về cấu trúc: ...</Field>
                <Field>Điểm đánh giá: x/10</Field>
            </Section>

            <Section title="Chi Tiết Đánh Giá">
                <IssueStructure>
                    <CriterionTitle>Tiêu đề (Title)</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Tóm tắt (Key Insights)</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Đặt vấn đề và Mục tiêu (Introduction & Objective)</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Trình bày chi tiết</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Kết luận</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
            </Section>>
            <Section title="Tổng Quan">
                <Field>Đánh giá tổng thể nội dung: ...</Field>
                <Field>Điểm đánh giá: x/10</Field>
            </Section>

            <Section title="Chi Tiết Đánh Giá">
                <IssueStructure>
                    <CriterionTitle>Key Insights</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Tổng quan về chủ đề</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Phân tích chi tiết</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Kết luận</CriterionTitle>
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
    with open("output/check_content.txt", "w", encoding="utf-8") as f:
        f.write(response.content)
    return response.content

def check_grammar_error(llm, text):
    """Kiểm tra lỗi ngữ pháp, chính tả, văn phong và các yêu cầu về nội dung liên quan đến web3, blockchain, crypto, và smart-contract."""
    
    prompt = f"""
    <EvaluationRequest>
        <Role>
            Bạn là một <strong>chuyên gia ngôn ngữ</strong> với kinh nghiệm đánh giá nội dung chuyên sâu trong lĩnh vực <strong>web3, blockchain, crypto, và smart-contract</strong>.
        </Role>

        <Mission>
            <Overview>
                Nhiệm vụ của bạn là <strong>kiểm tra và đánh giá văn phong, ngữ pháp, chính tả</strong> của bài viết, đảm bảo nội dung đạt tiêu chuẩn cao nhất về chất lượng và phù hợp với lĩnh vực chuyên môn.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Kiểm tra ngữ pháp và chính tả</Title>
                    <Details>
                        <Point>Phát hiện các lỗi ngữ pháp, chính tả, và dấu câu không hợp lý.</Point>
                        <Point>Đảm bảo câu cú rõ ràng, đúng ngữ pháp, không gây hiểu nhầm.</Point>
                        <Point>Trích dẫn nguyên văn câu bị lỗi và đề xuất cách sửa.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Kiểm tra văn phong và độ dài</Title>
                    <Details>
                        <Point>Đảm bảo văn phong chuyên nghiệp, phù hợp với lĩnh vực web3, blockchain, crypto, và smart-contract.</Point>
                        <Point>Kiểm tra độ dài bài viết, đảm bảo tối thiểu 2500 từ.</Point>
                        <Point>Phát hiện các đoạn văn quá dài hoặc quá ngắn, đề xuất cách chia nhỏ hoặc mở rộng nội dung.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Kiểm tra lỗi lặp từ</Title>
                    <Details>
                        <Point>Phát hiện lỗi lặp từ không cần thiết (trừ các từ khóa quan trọng).</Point>
                        <Point>Đề xuất cách thay thế từ đồng nghĩa hoặc cách diễn đạt khác để tránh lặp từ.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>4. Đánh giá tính mạch lạc và liên kết</Title>
                    <Details>
                        <Point>Đảm bảo các đoạn văn có liên kết logic, không rời rạc.</Point>
                        <Point>Kiểm tra xem các ý chính có được trình bày rõ ràng và mạch lạc không.</Point>
                        <Point>Đề xuất cách cải thiện nếu cần.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>5. Đề xuất cải thiện</Title>
                    <Details>
                        <Point>Nếu bài viết có thể cải thiện về văn phong, ngữ pháp, hoặc cách trình bày, hãy đưa ra gợi ý cụ thể.</Point>
                        <Point>Đảm bảo bài viết dễ đọc, dễ hiểu nhưng vẫn giữ được tính chuyên môn cao.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <OutputFormat>
            <Field>Trả lời bằng định dạng Markdown.</Field>
            <Field>Dịch 2 từ Analysis và FixSuggestion sang tiếng Việt</Field>
            <Section title="Tổng Quan">
                <Field>Đánh giá tổng thể về ngữ pháp, chính tả, và văn phong: ...</Field>
                <Field>Điểm đánh giá: x/10</Field>
            </Section>

            <Section title="Chi Tiết Đánh Giá">
                <IssueStructure>
                    <CriterionTitle>Ngữ pháp và chính tả</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Văn phong và độ dài</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Lỗi lặp từ</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Tính mạch lạc và liên kết</CriterionTitle>
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
    with open("output/check_grammar_error.txt", "w", encoding="utf-8") as f:
        f.write(response.content)
    return response.content

def check_keyword_distribution(llm,text):  
    """Kiểm tra phân bổ từ khóa trong bài viết."""  
    prompt = f"""
    <EvaluationRequest>
        <Role>
            Bạn là một <strong>chuyên gia SEO</strong> với kinh nghiệm tối ưu hóa nội dung để đạt hiệu suất cao trên công cụ tìm kiếm.
        </Role>

        <Mission>
            <Overview>
                Nhiệm vụ của bạn là <strong>kiểm tra và đánh giá việc phân bổ từ khóa</strong> trong bài viết, đảm bảo tối ưu cho SEO mà không bị nhồi nhét từ khóa (keyword stuffing).
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Xác định và phân tích từ khóa chính</Title>
                    <Details>
                        <Point>Từ khóa chính có xuất hiện trong tiêu đề (Title), thẻ H1, và Meta description không?</Point>
                        <Point>Từ khóa chính có xuất hiện trong 100 từ đầu tiên của bài viết không?</Point>
                        <Point>Từ khóa chính có được sử dụng tự nhiên, không gượng ép?</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Đánh giá phân bổ từ khóa trong nội dung</Title>
                    <Details>
                        <Point>Tỷ lệ từ khóa chính trên tổng số từ của bài viết có nằm trong khoảng 1-2% không?</Point>
                        <Point>Có sử dụng biến thể (LSI keywords) và từ đồng nghĩa thay vì lặp lại quá nhiều từ khóa chính không?</Point>
                        <Point>Các thẻ H2, H3 có chứa từ khóa phụ một cách hợp lý không?</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Phát hiện vấn đề và đề xuất cải thiện</Title>
                    <Details>
                        <Point>Nếu từ khóa chính bị lạm dụng (trên 2,5%), hãy chỉ ra các vị trí cần điều chỉnh.</Point>
                        <Point>Nếu bài viết thiếu từ khóa hoặc từ khóa phân bổ không hợp lý, hãy đề xuất cách cải thiện.</Point>
                        <Point>Gợi ý sử dụng từ đồng nghĩa và biến thể từ khóa để tránh lặp lại quá nhiều.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <OutputFormat>
            <Section title="Tổng Quan">
                <Field>Trả lời bằng định dạng Markdown.</Field>
                <Field>Đánh giá tổng thể về phân bổ từ khóa: ...</Field>
                <Field>Điểm đánh giá: x/10</Field>
            </Section>

            <Section title="Chi Tiết Đánh Giá">
                <IssueStructure>
                    <CriterionTitle>Xuất hiện trong Title, H1, Meta</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Xuất hiện trong 100 từ đầu tiên</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Mật độ từ khóa</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Keyword Stuffing</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Biến thể từ khóa & LSI</CriterionTitle>
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

def evaluate_readability(llm,text):  
    """Đánh giá độ dễ đọc và văn phong của bài viết."""  
    prompt = f"""
    <EvaluationRequest>
        <Role>
            Bạn là một <strong>chuyên gia ngôn ngữ và tối ưu hóa nội dung</strong> với kinh nghiệm đánh giá readability (độ dễ đọc) và văn phong của bài viết.
        </Role>

        <Mission>
            <Overview>
                Nhiệm vụ của bạn là <strong>đánh giá độ dễ đọc và văn phong của bài viết</strong>, đảm bảo nội dung rõ ràng, mạch lạc, dễ hiểu nhưng vẫn chuyên nghiệp và phù hợp với đối tượng mục tiêu.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Đánh giá độ dễ đọc (Readability)</Title>
                    <Details>
                        <Point>Tính toán điểm readability dựa trên tiêu chuẩn Flesch-Kincaid hoặc chỉ số tương đương.</Point>
                        <Point>Câu văn có quá dài, phức tạp hay không?</Point>
                        <Point>Sử dụng từ ngữ đơn giản, dễ hiểu hay mang tính học thuật quá cao?</Point>
                        <Point>Độ dài đoạn văn có hợp lý không? (Quá dài sẽ gây khó đọc)</Point>
                        <Point>Có sử dụng danh sách, gạch đầu dòng để tăng khả năng tiếp thu nội dung không?</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Đánh giá văn phong</Title>
                    <Details>
                        <Point>Văn phong có phù hợp với đối tượng độc giả không? (Chuyên môn cao, phổ thông, marketing...)</Point>
                        <Point>Ngôn ngữ có chính xác, khách quan, tránh cảm tính không?</Point>
                        <Point>Câu từ có rõ ràng, không mơ hồ hoặc gây hiểu lầm không?</Point>
                        <Point>Giọng văn có thống nhất không? (Tránh xen lẫn giữa trang trọng và thân mật)</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Đề xuất cải thiện</Title>
                    <Details>
                        <Point>Nếu câu văn quá dài hoặc phức tạp, hãy đề xuất cách viết lại súc tích hơn.</Point>
                        <Point>Nếu đoạn văn quá dày đặc, hãy gợi ý cách chia nhỏ thành đoạn hợp lý hơn.</Point>
                        <Point>Nếu bài viết thiếu danh sách hoặc ví dụ cụ thể, hãy đề xuất cách bổ sung.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <OutputFormat>
            <Section title="Tổng Quan">
                <Field>Đánh giá tổng thể readability: ...</Field>
                <Field>Điểm readability (theo thang Flesch-Kincaid hoặc tương đương): x/100</Field>
                <Field>Nhận xét chung về văn phong: ...</Field>
            </Section>

            <Section title="Chi Tiết Đánh Giá">
                <IssueStructure>
                    <CriterionTitle>Độ dài câu văn</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Độ dài đoạn văn</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Ngôn ngữ & mức độ dễ hiểu</CriterionTitle>
                    <Analysis>...</Analysis>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <IssueStructure>
                    <CriterionTitle>Văn phong & giọng điệu</CriterionTitle>
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

def check_uniqueness(llm,text):  
    """Kiểm tra tính độc nhất"""  
    prompt = f"""
    <EvaluationRequest>
        <Role>
            Bạn là một <strong>chuyên gia kiểm tra đạo văn và đánh giá tính độc nhất</strong> của nội dung bài viết.
        </Role>

        <Mission>
            <Overview>
                Nhiệm vụ của bạn là <strong>kiểm tra mức độ trùng lặp của nội dung</strong>, đảm bảo bài viết có tính độc nhất, không sao chép hoặc vay mượn quá nhiều từ các nguồn khác mà không có sự sáng tạo hoặc giá trị gia tăng.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Kiểm tra trùng lặp nội dung</Title>
                    <Details>
                        <Point>Phát hiện các đoạn có khả năng sao chép từ các nguồn khác.</Point>
                        <Point>So sánh với các văn bản phổ biến, tài liệu công khai, bài viết trên web.</Point>
                        <Point>Nếu có phần trùng lặp, hãy trích dẫn lại đoạn văn gốc và xác định mức độ trùng lặp.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Đánh giá tính độc nhất</Title>
                    <Details>
                        <Point>Bài viết có cung cấp quan điểm, phân tích hoặc cách diễn đạt riêng không?</Point>
                        <Point>Có sáng tạo hay chỉ đơn thuần lặp lại thông tin từ nguồn khác?</Point>
                        <Point>Nếu bài viết có trích dẫn tài liệu, có ghi nguồn rõ ràng không?</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Đề xuất chỉnh sửa nếu cần</Title>
                    <Details>
                        <Point>Nếu một đoạn có thể viết lại để khác biệt hơn, hãy đề xuất cách diễn đạt lại.</Point>
                        <Point>Nếu cần bổ sung nguồn trích dẫn, hãy chỉ ra vị trí cụ thể.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <OutputFormat>
            <Section title="Tổng Quan">
                <Field>Mức độ độc nhất: x%</Field>
                <Field>Nhận xét chung: ...</Field>
            </Section>

            <Section title="Chi Tiết Phát Hiện Trùng Lặp">
                <IssueStructure>
                    <OriginalText>"..."</OriginalText>
                    <Source>Phát hiện trùng với: [URL/Nguồn]</Source>
                    <SimilarityLevel>x%</SimilarityLevel>
                    <FixSuggestion>...</FixSuggestion>
                </IssueStructure>
                <!-- Lặp lại nếu có nhiều đoạn trùng lặp -->
            </Section>

            <Section title="Gợi Ý Cải Thiện">
                <FixStructure>
                    <OriginalText>"..."</OriginalText>
                    <SuggestedRewrite>...</SuggestedRewrite>
                    <Reason>...</Reason>
                </FixStructure>
                <!-- Lặp lại nếu cần -->
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

def check_internal_external_links(llm,text):  
    """Kiểm tra liên kết nội bộ và liên kết ngoài (internal & backlink)."""  
    pass  

def evaluate_research_depth(llm,text):  
    """Kiểm tra độ sâu nghiên cứu và mức độ dẫn chứng."""  
    prompt = f"""
    <EvaluationRequest>
        <Role>
            Bạn là một <strong>chuyên gia đánh giá nội dung</strong> với tiêu chuẩn cao, yêu cầu bài viết có <strong>nghiên cứu sâu</strong> và <strong>dẫn chứng thuyết phục</strong>.
        </Role>

        <Mission>
            <Overview>
                Bạn cần <strong>đánh giá độ sâu nghiên cứu</strong> của bài viết dưới đây, xem xét mức độ sử dụng tài liệu tham khảo, số liệu, và các dẫn chứng hỗ trợ lập luận.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Xác định mức độ nghiên cứu</Title>
                    <Details>
                        <Point>Bài viết có <strong>sử dụng tài liệu tham khảo không?</strong> (các nguồn đáng tin cậy như nghiên cứu khoa học, báo cáo, sách, bài báo chính thống).</Point>
                        <Point>Nếu không có tài liệu tham khảo, <strong>hãy chỉ ra điểm yếu</strong> và đề xuất nguồn tin phù hợp.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Đánh giá mức độ dẫn chứng</Title>
                    <Details>
                        <Point>Có **sử dụng số liệu, thống kê cụ thể** để hỗ trợ lập luận không?</Point>
                        <Point>Nếu có số liệu, **hãy kiểm tra xem nguồn có đáng tin không** (tránh Wikipedia, blog cá nhân, nguồn không rõ ràng).</Point>
                        <Point>Nếu bài viết chỉ đưa ra **lập luận chung chung, không có bằng chứng**, hãy chỉ ra điểm yếu và đề xuất cách cải thiện.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>3. Đánh giá so sánh và quan điểm đa chiều</Title>
                    <Details>
                        <Point>Bài viết có xem xét **các quan điểm khác nhau** về vấn đề không?</Point>
                        <Point>Nếu bài viết chỉ đưa ra một chiều quan điểm, hãy đề xuất cách bổ sung các góc nhìn khác để tăng tính khách quan.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>4. Kiểm tra mức độ phân tích chuyên sâu</Title>
                    <Details>
                        <Point>Bài viết có đi sâu vào vấn đề, đưa ra phân tích chi tiết không?</Point>
                        <Point>Nếu chỉ dừng ở mô tả bề mặt, hãy đề xuất cách đi sâu hơn vào từng điểm chính.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <Criteria>
            <Criterion>
                <Title>1. Nghiên cứu & Nguồn tham khảo (10 điểm)</Title>
                <Checklist>
                    <Item>Có sử dụng nguồn tài liệu tin cậy?</Item>
                    <Item>Tránh tuyệt đối Wikipedia, blog cá nhân?</Item>
                </Checklist>
            </Criterion>

            <Criterion>
                <Title>2. Mức độ dẫn chứng (10 điểm)</Title>
                <Checklist>
                    <Item>Có sử dụng số liệu, thống kê không?</Item>
                    <Item>Nguồn số liệu có uy tín không?</Item>
                </Checklist>
            </Criterion>

            <Criterion>
                <Title>3. So sánh và quan điểm đa chiều (10 điểm)</Title>
                <Checklist>
                    <Item>Có xem xét quan điểm khác không?</Item>
                    <Item>Có phân tích sự khác biệt giữa các quan điểm không?</Item>
                </Checklist>
            </Criterion>

            <Criterion>
                <Title>4. Độ sâu phân tích (10 điểm)</Title>
                <Checklist>
                    <Item>Có đi sâu vào vấn đề không?</Item>
                    <Item>Hay chỉ dừng lại ở mô tả bề mặt?</Item>
                </Checklist>
            </Criterion>
        </Criteria>

        <OutputFormat>
            <Section title="Tổng Quan">
                <Field>Tổng điểm: .../40</Field>
                <Field>Nhận xét chung: ...</Field>
            </Section>

            <Section title="Chi Tiết Từng Tiêu Chí">
                <CriterionEvaluation>
                    <CriterionTitle>1. Nghiên cứu & Nguồn tham khảo: x/10</CriterionTitle>
                    <Pros>✅ Ưu điểm: ...</Pros>
                    <Cons>❌ Vấn đề: ...</Cons>
                    <Suggestions>💡 Gợi ý chỉnh sửa: ...</Suggestions>
                </CriterionEvaluation>

                <CriterionEvaluation>
                    <CriterionTitle>2. Mức độ dẫn chứng: x/10</CriterionTitle>
                    <Pros>✅ Ưu điểm: ...</Pros>
                    <Cons>❌ Vấn đề: ...</Cons>
                    <Suggestions>💡 Gợi ý chỉnh sửa: ...</Suggestions>
                </CriterionEvaluation>

                <CriterionEvaluation>
                    <CriterionTitle>3. So sánh và quan điểm đa chiều: x/10</CriterionTitle>
                    <Pros>✅ Ưu điểm: ...</Pros>
                    <Cons>❌ Vấn đề: ...</Cons>
                    <Suggestions>💡 Gợi ý chỉnh sửa: ...</Suggestions>
                </CriterionEvaluation>

                <CriterionEvaluation>
                    <CriterionTitle>4. Độ sâu phân tích: x/10</CriterionTitle>
                    <Pros>✅ Ưu điểm: ...</Pros>
                    <Cons>❌ Vấn đề: ...</Cons>
                    <Suggestions>💡 Gợi ý chỉnh sửa: ...</Suggestions>
                </CriterionEvaluation>
            </Section>
        </OutputFormat>

        <Content>
            --- BẮT ĐẦU BÀI VIẾT CẦN ĐÁNH GIÁ ---
            {text}
            --- KẾT THÚC BÀI VIẾT ---
        </Content>
    </EvaluationRequest>
    """
    
    # Invoke the LLM with the evaluation criteria and content
    response = llm.invoke(prompt)
    return response.content

def check_logic_and_objectivity(llm,text):  
    """Kiểm tra logic và tính khách quan của bài viết."""  
    pass  

def check_grammar_and_spelling(llm,text):  
    """Kiểm tra ngữ pháp và lỗi chính tả."""  
    pass  

def check_conclusion_and_cta(llm,text):  
    """Kiểm tra phần kết luận và lời kêu gọi hành động (CTA)."""  
    pass  

# Function to evaluate the content of a PDF based on predefined criteria using an LLM
def ContentCheck(llm, text):
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
            Bạn là một <strong>chuyên gia đánh giá nội dung khó tính, kỹ tính và có chuyên môn cao</strong> trong lĩnh vực <strong>blockchain, crypto, smart contract</strong>.
        </Role>

        <Mission>
            <Overview>
                Bạn cần <strong>phân tích, chấm điểm và góp ý chỉnh sửa chi tiết</strong> nội dung bài viết dưới đây dựa trên các tiêu chí học thuật.
            </Overview>

            <Instructions>
                <Instruction>
                    <Title>1. Chấm điểm từng tiêu chí theo thang điểm 10, tổng điểm tối đa là 100.</Title>
                    <Details>
                        <Point>Nếu chấm dưới 8 điểm, cần nói rõ <strong>lý do mất điểm</strong>.</Point>
                        <Point>Nếu nội dung tốt nhưng có thể nâng cấp, <strong>hãy đưa ra gợi ý để xuất sắc hơn nữa</strong>.</Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>2. Chỉ ra các vấn đề cụ thể trong bài viết:</Title>
                    <Details>
                        <Point>Những câu từ <strong>thiếu chính xác, cảm tính, mơ hồ, thiếu dẫn chứng</strong>.</Point>
                        <Point>**Luôn kiểm tra ngữ cảnh xung quanh** (các đoạn trước và sau) trước khi nhận định một câu là mơ hồ hoặc thiếu thông tin.</Point>
                        <Point>Các đoạn <strong>trôi chảy nhưng hời hợt, thiếu chiều sâu phân tích hoặc thiếu liên kết logic</strong>.</Point>
                        <Point>Những nội dung <strong>lặp lại, dư thừa hoặc gây hiểu nhầm</strong>.</Point>
                    </Details>
                    <ErrorHandling>
                        <Point>Trích nguyên văn đoạn văn có vấn đề (nếu có thể).</Point>
                        <Point>Không đánh giá một câu là “thiếu dẫn chứng” hoặc “mơ hồ” nếu phần dẫn chứng nằm ở đoạn liền kề trước hoặc sau đó.</Point>
                        <Point>Nếu nghi ngờ, hãy trích thêm đoạn trên/dưới để kiểm tra ngữ cảnh.</Point>
                        <Point>Giải thích vì sao đoạn đó chưa ổn.</Point>
                        <Point>Gợi ý viết lại hoặc chỉnh sửa hợp lý hơn.</Point>
                    </ErrorHandling>
                </Instruction>

                <Instruction>
                    <Title>3. Trình bày kết quả bằng Markdown</Title>
                    <Details>
                        <Point>Sử dụng biểu tượng:
                            <Symbols>
                                <Symbol>✅ Ưu điểm</Symbol>
                                <Symbol>❌ Vấn đề</Symbol>
                                <Symbol>💡 Gợi ý chỉnh sửa</Symbol>
                            </Symbols>
                        </Point>
                    </Details>
                </Instruction>

                <Instruction>
                    <Title>4. Kiểm tra ngữ pháp và chính tả</Title>
                    <Details>
                        <Point>Phát hiện và liệt kê các lỗi chính tả, ngữ pháp, dùng sai từ, lặp từ, hoặc dấu câu không hợp lý.</Point>
                        <Point>Nếu có lỗi, hãy trích nguyên văn câu từ bị lỗi và đề xuất cách viết đúng hơn.</Point>
                        <Point>Nếu bài viết viết tốt, vẫn nên chỉ ra một số đoạn nên viết lại cho mượt hơn.</Point>
                    </Details>
                </Instruction>
            </Instructions>
        </Mission>

        <Criteria>
            <Criterion>
                <Title>1. Nội dung và Mục tiêu Rõ Ràng (10 điểm)</Title>
                <Checklist>
                    <Item>Có mục tiêu rõ ràng không?</Item>
                    <Item>Đối tượng người đọc có được xác định?</Item>
                    <Item>Vấn đề có thực tiễn và mang lại giá trị thiết thực không?</Item>
                </Checklist>
            </Criterion>

            <Criterion>
                <Title>2. Độ Sâu của Nghiên Cứu và Tài Liệu Tham Khảo (10 điểm)</Title>
                <Checklist>
                    <Item>Có dẫn nguồn tin cậy không?</Item>
                    <Item>Có sử dụng các quan điểm trái chiều không?</Item>
                    <Item>Tránh tuyệt đối Wikipedia, blog cá nhân?</Item>
                </Checklist>
            </Criterion>

            <Criterion>
                <Title>3. Cấu Trúc Hợp Lý và Logic (10 điểm)</Title>
                <Checklist>
                    <Item>Có các phần chính như: Tiêu đề, Tóm tắt, Giới thiệu, Phân tích, Kết luận?</Item>
                    <Item>Các phần có liên kết logic, trình bày có mạch lạc không?</Item>
                </Checklist>
            </Criterion>

            <Criterion>
                <Title>4. Phân Tích Chuyên Sâu và Có Dữ Liệu Hỗ Trợ (20 điểm)</Title>
                <Checklist>
                    <Item>Có đưa ra số liệu cụ thể?</Item>
                    <Item>Phân tích có chiều sâu?</Item>
                    <Item>Có so sánh với đối thủ không?</Item>
                </Checklist>
            </Criterion>

            <Criterion>
                <Title>5. Tính Khách Quan và Hợp Lý (10 điểm)</Title>
                <Checklist>
                    <Item>Tránh thiên kiến, cảm tính?</Item>
                    <Item>Đánh giá trung lập, dựa trên dữ kiện?</Item>
                </Checklist>
            </Criterion>

            <Criterion>
                <Title>6. Văn Phong và Trình Bày (10 điểm)</Title>
                <Checklist>
                    <Item>Văn phong chuyên nghiệp, dễ hiểu?</Item>
                    <Item>Có heading rõ ràng, gạch đầu dòng?</Item>
                    <Item>Giải thích thuật ngữ kỹ thuật?</Item>
                    <Item>Độ dài ≥ 2500 từ?</Item>
                </Checklist>
            </Criterion>

            <Criterion>
                <Title>7. Đánh Giá Kết Quả và Đề Xuất Hành Động (10 điểm)</Title>
                <Checklist>
                    <Item>Kết luận có tổng hợp lại ý chính?</Item>
                    <Item>Có nêu tiềm năng, rủi ro, bước tiếp theo không?</Item>
                </Checklist>
            </Criterion>

            <Criterion>
                <Title>8. Ngôn ngữ và Chính tả (10 điểm)</Title>
                <Checklist>
                    <Item>Chính tả đúng, không lỗi đánh máy?</Item>
                    <Item>Câu cú rõ ràng, đúng ngữ pháp?</Item>
                    <Item>Tránh lặp từ, dùng từ sai hoặc không phù hợp ngữ cảnh?</Item>
                    <Item>Dấu câu hợp lý, trình bày dễ đọc?</Item>
                </Checklist>
            </Criterion>
        </Criteria>

        <OutputFormat>
            <Section title="Tổng Quan">
                <Field>Tổng điểm: .../100</Field>
                <Field>Nhận xét chung: ...</Field>
            </Section>

            <Section title="Chi Tiết Từng Tiêu Chí">
                <CriterionEvaluation>
                    <CriterionTitle>1. Nội dung và Mục tiêu Rõ Ràng: x/10</CriterionTitle>
                    <Pros>✅ Ưu điểm: ...</Pros>
                    <Cons>❌ Vấn đề: ...</Cons>
                    <Suggestions>💡 Gợi ý chỉnh sửa: ...</Suggestions>
                </CriterionEvaluation>
                <!-- Lặp lại cho các tiêu chí khác -->
            </Section>

            <Section title="Các Vị Trí Câu Từ Cần Cải Thiện">
                <IssueStructure>
                    <OriginalText>"Dự án này cực kỳ tiềm năng vì ai cũng nhắc đến"</OriginalText>
                    <Problem>Thiếu căn cứ, cảm tính</Problem>
                    <FixSuggestion>Nên đưa số liệu cụ thể, ví dụ TVL tăng, user active,... để chứng minh</FixSuggestion>
                </IssueStructure>
                <!-- có thể lặp lại -->
            </Section>

            <Section title="Các Lỗi Ngữ Pháp và Chính Tả">
                <IssueStructure>
                    <OriginalText>"Tuy nhiên, dự án lại có một vấn đề nhỏ nhưng quan trong."</OriginalText>
                    <Problem>Lỗi chính tả: "quan trong" → "quan trọng"</Problem>
                    <FixSuggestion>Viết lại: "Tuy nhiên, dự án lại có một vấn đề nhỏ nhưng quan trọng."</FixSuggestion>
                </IssueStructure>
                <!-- có thể lặp lại -->
            </Section>

        </OutputFormat>

        <Note>
            <Point>Không ghi lại các ví dụ mẫu.</Point>
            <Point>Nếu bài viết không đề cập đến nội dung của một tiêu chí nào, bạn có thể bỏ qua tiêu chí đó nhưng phải ghi rõ lý do.</Point>
            <Point>Tránh đánh giá tách rời từng câu. Một câu có thể là mở đầu cho đoạn giải thích phía sau.</Point>
            <Point>Đánh giá trung thực, không xu nịnh. Nếu bài tốt, hãy khen đúng chỗ, nếu dở, hãy góp ý cụ thể.</Point>
            <Point>Nếu bài tốt nhưng chưa xuất sắc, hãy đưa ra cách để giúp nó <strong>vượt chuẩn</strong>.</Point>
        </Note>

        <Content>
        --- BẮT ĐẦU BÀI VIẾT CẦN ĐÁNH GIÁ ---
        {text}
        --- KẾT THÚC BÀI VIẾT ---
        </Content>
    </EvaluationRequest>
    """

    # Invoke the LLM with the evaluation criteria and content
    response = llm.invoke(require)
    return response.content

def check_text(llm,text):
    """Tổng kiểm tra nội dung bài viết"""

    check_article_structure_result=check_article_structure(llm,text)
    check_content_result=check_content(llm,text)
    check_grammar_error_result=check_grammar_error(llm,text)

    sumarize_result = f"""
    Kết quả kiểm tra cấu trúc theo yêu cầu bài viết:
    {check_article_structure_result}

    Kết quả kiểm tra nội dung theo yêu cầu bài viết:
    {check_content_result}

    Kết quả kiểm tra ngữ pháp, chính tả, văn phong, độ dài:
    {check_grammar_error_result}
    """

    with open("output/check_text.txt", "w", encoding="utf-8") as f:
        f.write(sumarize_result)

    return sumarize_result

if __name__ == "__main__":
    import os
    import extract
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
    text = extract.extract_text(pdf_path)

    # check_article_structure(llm, text)

    # check_content(llm,text)

    # check_grammar_error(llm,text)

    check_text(llm,text)