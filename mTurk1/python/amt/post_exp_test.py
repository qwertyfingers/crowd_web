from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer
 

def post_HIT1(ACCESS_ID,SECRET_KEY,HOST,url_to_task):
    mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)
 
    title = 'Dev deploying simulation test Report From SERVER'
    description = ('Report on events in a simulation')
    keywords = 'website, rating, opinions'
    instructions=('<p>You will take part in a web-based experiment where you will watch a simple simulation and provide reports on events</p>'
                 '<p>Instructions:</p>'
                  '<p>1. Click the link below, which will open the webpage in a new window in your browser</p>'
                  '<p>2. Follow the instructions on the website</p>'
                  '<p>3. Once you have completed your work, you will receive a Reward Code</p>'
                  '<p>4. Return to the mechanical turk webpage and enter your code in the Reward Code text box</p>'
                  '<p>5. Your work will then be checked, after which you will receive your payment</p>'
                  '<br/>CLICK "ACCEPT HIT" BEFORE FOLLOWING LINK'
                  '<br/>YOU WILL NOT BE PAID WITHOUT ACCEPTING THE HIT')
                    
                    
    #---------------  BUILD OVERVIEW -------------------
     
    overview = Overview()
    overview.append_field('Title', description)
    overview.append(FormattedContent(instructions))
    overview.append(FormattedContent('<p>Click "Accept HIT" then click this link <a target="_blank"'
                                     ' href="'+url_to_task+'">'
                                     ' Link to task</a></p>'))
 
    #---------------  BUILD QUESTION 1 -------------------
     
    qc1 = QuestionContent()
    qc1.append_field('Title','Enter reward code here:')
     
    fta1 = FreeTextAnswer(num_lines=1)
    
    q1 = Question(identifier='reward_code',
                  content=qc1,
                  answer_spec=AnswerSpecification(fta1),
                  is_required=True)
     
     
    #--------------- BUILD THE QUESTION FORM -------------------
     
    question_form = QuestionForm()
    question_form.append(overview)
    question_form.append(q1)
    
     
    #--------------- CREATE THE HIT -------------------
     
    mtc.create_hit(questions=question_form,
                   max_assignments=1,
                   title=title,
                   description=description,
                   keywords=keywords,
                   duration = 60*5,
                   reward=0.05)