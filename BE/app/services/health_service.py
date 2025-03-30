import psutil


class HealthService:
    GREEN_CPU_PERCENTAGE_MAX = 60
    GREEN_MEMORY_PERCENTAGE_MAX = 70
    GREEN_DISK_USAGE_PERCENTAGE_MAX = 75

    YELLOW_CPU_PERCENTAGE_MAX = 85
    YELLOW_MEMORY_PERCENTAGE_MAX = 90
    YELLOW_DISK_USAGE_PERCENTAGE_MAX = 90

    @classmethod
    def get_system_stats(cls):
        return {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage("/").percent,
        }

    @classmethod
    def calculate_system_status(cls):
        system_data = cls.get_system_stats()
        if (
            system_data.get("cpu_usage") < cls.GREEN_CPU_PERCENTAGE_MAX
            and system_data.get("memory_usage") < cls.GREEN_MEMORY_PERCENTAGE_MAX
            and system_data.get("disk_usage") < cls.GREEN_DISK_USAGE_PERCENTAGE_MAX
        ):
            return "green"
        elif (
            system_data.get("cpu_usage") < cls.YELLOW_CPU_PERCENTAGE_MAX
            and system_data.get("memory_usage") < cls.YELLOW_MEMORY_PERCENTAGE_MAX
            and system_data.get("disk_usage") < cls.YELLOW_DISK_USAGE_PERCENTAGE_MAX
        ):
            return "yellow"
        else:
            return "red"
