import matplotlib.pyplot as plt


def plot_skill_stats(skill_stats, top_n=15):
    top_skills = skill_stats[:top_n]
    skills, counts = zip(*top_skills)

    plt.figure(figsize=(12, 6))
    plt.bar(skills, counts, color="skyblue")
    plt.title("Top Demanded Skills in French Dev Jobs")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('data/skills_chart.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Chart saved as 'skills_chart.png'")
