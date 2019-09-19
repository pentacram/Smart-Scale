from .models import *
import matplotlib.pyplot as plt


# InfoField = None

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


def analyze_data(cow_id, from_date, to_date):
    try:
        df = InfoFields.objects.filter(id=cow_id, date__gte=from_date, date__lte=to_date).values()

        # df = [{'date': datetime.today(), 'weight': 100.2}, {'date': datetime(2019, 9, 17), 'weight': 83.2}, {'date': datetime(2019, 9, 15), 'weight': 83.2}, \
        # {'date': datetime(2019, 9, 16), 'weight': 100.2}]

        date = [x['date'].strftime('%d/%m/%y') for x in df]
        weight = [x['weight'] for x in df]

        plt.scatter(date, weight)
        plt.title('Zaman-Çəki asılılığı')
        plt.xticks(rotation=90)
        plt.xlabel('Tarix')
        plt.ylabel('Çəki (kg)')

        graph_name = str(cow_id) + '.png'
        plt.savefig(graph_name)

        maxWeight, maxWeightDate = max(df, key=lambda x: x['weight']).values()
        minWeight, minWeightDate = min(df, key=lambda x: x['weight']).values()

        meanWeight = mean([x['weight'] for x in df])

        data = {'pic': graph_name, 'max_weight': maxWeight, 'max_weight_date': maxWeightDate, \
                'min_weight': minWeight, 'min_weight_date': minWeightDate, 'mean_weight': meanWeight}
        return data
    except Exception:
        print('data not found')


print(analyze_data(0, 0, 0))