import streamlit as st
import pandas as pd
import os

# اسم ملف الإكسيل
FILE_NAME = "shoes_inventory_system.xlsx"


# وظيفة تحميل البيانات أو إنشاء ملف جديد
def load_data():
    if os.path.exists(FILE_NAME):
        return pd.read_excel(FILE_NAME)
    else:
        # إنشاء الأعمدة الأساسية
        return pd.DataFrame(columns=["النوع", "المنتج", "المقاس", "السعر الأساسي", "سعر البيع", "الكمية", "صافي الربح"])


# تحميل البيانات
df = load_data()

st.set_page_config(page_title="ضجه", layout="wide")
st.title("👞 ضجه")

# القائمة الجانبية
menu = st.sidebar.radio("القائمة", ["لوحة التحكم", "إضافة بضاعة جديدة", "تسجيل مبيعات"])

if menu == "لوحة التحكم":
    st.subheader("📊 ملخص المخزون والأرباح")

    # حسابات سريعة
    if not df.empty:
        total_qty = df["الكمية"].sum()
        total_profit = df["صافي الربح"].sum()

        col1, col2 = st.columns(2)
        col1.metric("إجمالي القطع في المحل", f"{int(total_qty)}")
        col2.metric("إجمالي الأرباح", f"{total_profit:,} جنيه")

        st.dataframe(df)
    else:
        st.info("لا توجد بيانات حالياً.")

elif menu == "إضافة بضاعة جديدة":
    st.subheader("➕ إضافة صنف جديد")
    with st.form("add_item_form"):
        category = st.selectbox("نوع الصنف", ["كاوتشات", "شباشب", "أحذية كلاسيك", "أحذية أطفال"])
        name = st.text_input("اسم الموديل")
        size = st.text_input("المقاس")
        cost = st.number_input("سعر الشراء (الأساسي)", min_value=0.0)
        price = st.number_input("سعر البيع", min_value=0.0)
        qty = st.number_input("الكمية", min_value=1)

        if st.form_submit_button("إضافة للمخزن"):
            new_item = pd.DataFrame([[category, name, size, cost, price, qty, 0.0]], columns=df.columns)
            df = pd.concat([df, new_item], ignore_index=True)
            df.to_excel(FILE_NAME, index=False)
            st.success("تمت الإضافة بنجاح!")

elif menu == "تسجيل مبيعات":
    st.subheader("💰 تسجيل عملية بيع")
    if not df.empty:
        with st.form("sell_form"):
            prod = st.selectbox("اختر الصنف", df["المنتج"].unique())
            qty_sold = st.number_input("الكمية المباعة", min_value=1)

            submit_button = st.form_submit_button("إتمام البيع")

            if submit_button:
                # البحث عن صف المنتج
                idx = df[df["المنتج"] == prod].index[0]
                if df.at[idx, "الكمية"] >= qty_sold:
                    # حساب الربح وتحديث البيانات
                    profit = (df.at[idx, "سعر البيع"] - df.at[idx, "السعر الأساسي"]) * qty_sold
                    df.at[idx, "الكمية"] -= qty_sold
                    df.at[idx, "صافي الربح"] += profit
                    df.to_excel(FILE_NAME, index=False)
                    st.success(f"تم تسجيل البيع بنجاح! الربح من العملية: {profit} جنيه")
                else:
                    st.error("الكمية في المخزن لا تكفي!")
    else:
        st.warning("لا توجد بضاعة في المخزن حالياً.")