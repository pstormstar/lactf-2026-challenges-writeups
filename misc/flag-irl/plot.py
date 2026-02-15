import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_final_filtered():
    OBJ1_MIN, OBJ1_MAX = 925, 1100  
    OBJ2_MIN, OBJ2_MAX = 850, 1080    

    df = pd.read_csv("results.csv")
    df['Obj1_X'] = pd.to_numeric(df['Obj1_X'], errors='coerce')
    df['Obj2_X'] = pd.to_numeric(df['Obj2_X'], errors='coerce')
    df = df.dropna(subset=['Obj1_X', 'Obj2_X']).reset_index(drop=True)

    spatial_mask = (
        (df['Obj1_X'] >= OBJ1_MIN) & (df['Obj1_X'] <= OBJ1_MAX) &
        (df['Obj2_X'] >= OBJ2_MIN) & (df['Obj2_X'] <= OBJ2_MAX)
    )
    df = df[spatial_mask].reset_index(drop=True)
    dist_prev = np.sqrt((df['Obj1_X'] - df['Obj1_X'].shift(1))**2 + (df['Obj2_X'] - df['Obj2_X'].shift(1))**2)
    dist_next = np.sqrt((df['Obj1_X'] - df['Obj1_X'].shift(-1))**2 + (df['Obj2_X'] - df['Obj2_X'].shift(-1))**2)
    
    point_mask = (dist_prev.fillna(0) <= 4) & (dist_next.fillna(0) <= 4)
    df_clean = df[point_mask].reset_index(drop=True)

    final_data = []
    for i in range(len(df_clean)):
        if i > 0:
            gap = np.sqrt((df_clean.loc[i, 'Obj1_X'] - df_clean.loc[i-1, 'Obj1_X'])**2 + 
                            (df_clean.loc[i, 'Obj2_X'] - df_clean.loc[i-1, 'Obj2_X'])**2)
            
            if gap > 4:
                final_data.append({'Obj1_X': np.nan, 'Obj2_X': np.nan})
        
        final_data.append({'Obj1_X': df_clean.loc[i, 'Obj1_X'], 'Obj2_X': df_clean.loc[i, 'Obj2_X']})

    df_final = pd.DataFrame(final_data)
    plt.figure(figsize=(10, 8))
    
    plt.plot(df_final['Obj2_X'], df_final['Obj1_X'], 
                color='teal', marker='o', markersize=2, linestyle='-', alpha=0.6)

    plt.gca().invert_yaxis()

    plt.title(f'Filtered Relationship (Jump Limit: 4px)')
    plt.xlabel('Object 2 X-Position')
    plt.ylabel('Object 1 X-Position (Mirrored)')

    plt.grid(True, which='both', linestyle=':', alpha=0.5)
    plt.axis('equal')
    
    print(f"Points after distance filter: {len(df_final)}")
    plt.show()

if __name__ == "__main__":
    plot_final_filtered()