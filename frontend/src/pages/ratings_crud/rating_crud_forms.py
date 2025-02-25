import streamlit as st
from backend.controller.rating_controller import RatingController
from backend.view.rating import Rating
import uuid  

ratingController = RatingController()

def show_create_rating():
    """Form for submitting a rating with validation."""

    st.title("Submit a Rating")

    # Star rating input (0 to 5)
    rating = st.slider("Rating (0 to 5 Stars)", min_value=0, max_value=5, step=1)

    # Text input for comment
    comment = st.text_area("Comment", placeholder="Write your feedback here...")

    # Dropdown for final_feeling
    final_feeling_options = [ "Very Good","Good", "Neutral", "Bad", "Very Bad"]
    final_feeling = st.selectbox("Final Feeling", final_feeling_options)

    # Checkbox for recommendation
    recommend = st.checkbox("Would you recommend this?", value=False)

    # Submit button
    if st.button("Submit Rating"):
        # Validation
        if rating is None:
            st.error("Please provide a rating.")
        elif comment.strip() == "":
            st.error("Comment cannot be empty.")
        elif final_feeling not in final_feeling_options:
            st.error("Invalid final feeling selected.")
        else:
            rating_id = str(uuid.uuid4())
            rating = Rating(
                rating_id= rating_id,
                rating=rating,
                comment=comment,
                final_feeling=final_feeling,
                recommend=recommend
            )
            
            ratingController.create_rating(
                rating=rating
            )
            # If all validations pass, process submission
            st.success("Rating submitted successfully! ✅")
            st.write("### Submitted Data:")
            st.json({
                "rating_id" : rating_id,
                "rating": rating,
                "comment": comment,
                "final_feeling": final_feeling,
                "recommend": recommend
            })

def show_read_rating():
    pass 

def show_update_rating():
    pass 

def show_delete_rating():
    pass 


