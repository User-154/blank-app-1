import streamlit as st
import pandas as pd
import numpy as np

def main():
    st.title("Экспертная оценка приоритетных направлений ответа на западные санкции")
    st.write("""
    Санкционное давление создало значительные вызовы для экономики России, такие как низкие цены на нефть, 
    бизнес лишился доступа к длинным и дешевым кредитам, ослабление национальной валюты и общее замедление 
    экономического роста. Необходимо определить наиболее эффективные и приоритетные направления государственной 
    политики и стратегии бизнеса для противодействия негативным последствиям санкций и обеспечения устойчивого 
    и суверенного развития страны в новых условиях.
    """)

    alternatives = {
        'A': 'Импортозамещение товарами, произведенными внутри России',
        'B': 'Диверсификация экспорта и поиск новых рынков',
        'C': 'Повышение ключевой ставки по кредитам и вкладам центральным банком',
        'D': 'Создание госпрограмм поддержки малого и среднего бизнеса',
        'E': 'Развитие национальной финансовой системы и отказа от доллара',
        'F': 'Ограничение вывода денег за пределы страны',
        'G': 'Политическое сотрудничество и дипломатия',
        'H': 'Использование криптовалюты и альтернативных платежных систем'
    }
    
    st.header("Метод полного попарного сопоставления")
    st.write("""
    **Инструкция:** Для каждой пары направлений оцените, насколько первое направление предпочтительнее второго 
    по шкале от 1 до 10, где:
    - 1: второе направление абсолютно предпочтительнее первого
    - 5: направления равнозначны
    - 10: первое направление абсолютно предпочтительнее второго
    """)
    
    expert_name = st.text_input("Введите ваше имя (эксперт):")
    
    if not expert_name:
        st.warning("Пожалуйста, введите ваше имя для продолжения.")
        return
    
    n = len(alternatives)
    alt_keys = list(alternatives.keys())
    
    st.subheader("Попарное сравнение направлений")
    
    comparisons = {}
    
    for i in range(n):
        for j in range(i + 1, n):
            key1 = alt_keys[i]
            key2 = alt_keys[j]
            pair_key = f"{key1}_{key2}"
            
            col1, col2, col3 = st.columns([2, 1, 2])
            
            with col1:
                st.write(f"**{alternatives[key1]}**")
            with col2:
                rating = st.slider(
                    f"Сравнение {key1} и {key2}",
                    min_value=1,
                    max_value=10,
                    value=5,
                    key=pair_key
                )
            with col3:
                st.write(f"**{alternatives[key2]}**")
            
            comparisons[pair_key] = rating
    
    if st.button("Рассчитать результаты"):
        P = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    P[i, j] = 0
                else:
                    key1 = alt_keys[i]
                    key2 = alt_keys[j]
                    pair_key = f"{key1}_{key2}" if i < j else f"{key2}_{key1}"
                    
                    if i < j:
                        rating = comparisons[pair_key]
                        P[i, j] = rating / 10
                    else:
                        rating = comparisons[pair_key]
                        P[i, j] = (10 - rating) / 10
        
        f_scores = np.sum(P, axis=1)
        
        N = n * (n - 1)
        g_scores = f_scores / N
        
        results_df = pd.DataFrame({
            'Направление': [alternatives[key] for key in alt_keys],
            'Код': alt_keys,
            'f_score': f_scores,
            'g_score': g_scores
        })
        
        results_df = results_df.sort_values('g_score', ascending=False)
        results_df['Ранг'] = range(1, len(results_df) + 1)
        
        st.subheader("Результаты оценки эксперта")
        st.write(f"**Эксперт:** {expert_name}")
        
        st.write("**Матрица частот P:**")
        matrix_df = pd.DataFrame(P, 
                               index=[f"{key}: {alternatives[key][:30]}..." for key in alt_keys],
                               columns=alt_keys)
        st.dataframe(matrix_df.style.format("{:.2f}"))
        
        st.write("**Оценки предпочтения:**")
        display_df = results_df[['Ранг', 'Код', 'Направление', 'f_score', 'g_score']].reset_index(drop=True)
        st.dataframe(display_df.style.format({'f_score': '{:.2f}', 'g_score': '{:.4f}'}))
        
        st.subheader("Визуализация приоритетов")
        
        fig_df = results_df.copy()
        fig_df = fig_df.sort_values('g_score', ascending=True)
        
        st.bar_chart(fig_df.set_index('Направление')['g_score'])
    
        st.subheader("Ранжированный список направлений")
        for idx, row in results_df.iterrows():
            st.write(f"{row['Ранг']}. **{row['Код']}**: {row['Направление']} (g_score: {row['g_score']:.4f})")
        
        st.subheader("Анализ результатов")
        st.write(f"**Наиболее приоритетное направление:** {results_df.iloc[0]['Код']} - {results_df.iloc[0]['Направление']}")
        st.write(f"**Наименее приоритетное направление:** {results_df.iloc[-1]['Код']} - {results_df.iloc[-1]['Направление']}")
        
        if st.button("Сохранить результаты"):
            st.success("Результаты сохранены!")

if __name__ == "__main__":
    main()