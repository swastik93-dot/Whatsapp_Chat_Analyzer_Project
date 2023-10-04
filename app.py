import streamlit as st
import Preprocessor
import helper
import matplotlib.pyplot as plt

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = Preprocessor.preprocess(data)

    st.dataframe(df)
    user_list = df['user'].unique().tolist()

    if 'group_notification' in user_list:
        user_list.remove('group_notification')

    user_list.sort()
    user_list.insert(0, "Overall")

























    selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages = helper.fetch_stats(selected_user, df)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Messages")
            st.subheader(num_messages)
        with col2:
            st.subheader("Total Words")
            st.subheader(words)
        with col3:
            st.subheader("Media Shared")
            st.subheader(num_media_messages)

    # Finding busiest user in the group
    if selected_user == 'Overall':
        st.title('Most Busy Users')
        x, new_df = helper.most_busy_users(df)
        fig, ax = plt.subplots()
        col1, col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)

    # Word Cloud
    st.title("Word Cloud")
    df_wc = helper.create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    plt.imshow(df_wc)
    plt.axis('off')
    st.pyplot(fig)

    # Most common words
    st.title("Most common words")
    most_common_df = helper.most_common_words(selected_user, df)

    fig,ax = plt.subplots()
    ax.bar(most_common_df[0],most_common_df[1])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

