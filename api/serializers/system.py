from rest_framework import serializers

class HealthCheckSerializer(serializers.Serializer):
	status = serializers.CharField()
	timestamp = serializers.DateTimeField()
	service = serializers.CharField()
	version = serializers.CharField()


class DatabaseInfoSerializer(serializers.Serializer):
	connected = serializers.BooleanField()
	engine = serializers.CharField(allow_null=True)
	name = serializers.CharField(required=False)
	host = serializers.CharField(required=False)
	error = serializers.CharField(required=False)

class CacheInfoSerializer(serializers.Serializer):
	connected = serializers.BooleanField()
	backend = serializers.CharField(required=False)
	error = serializers.CharField(required=False)

class DiskInfoSerializer(serializers.Serializer):
	percent_gb = serializers.FloatField()
	used_gb = serializers.FloatField()
	free_gb = serializers.FloatField()
	total_gb = serializers.FloatField()

class MemoryInfoSerializer(serializers.Serializer):
	percent_gb = serializers.FloatField()
	used_gb = serializers.FloatField()
	free_gb = serializers.FloatField()
	total_gb = serializers.FloatField()

class CpuInfoSerializer(serializers.Serializer):
	percent = serializers.FloatField()
	count = serializers.IntegerField()
	architecture = serializers.CharField()
	processor_type = serializers.CharField()

class SystemInfoSerializer(serializers.Serializer):
	system = serializers.CharField()
	status = serializers.CharField()
	timestamp = serializers.DateTimeField()
	uptime_server = serializers.CharField()
	python = serializers.CharField()
	django = serializers.CharField()
	memory_usage = MemoryInfoSerializer()
	disk_usage = DiskInfoSerializer()
	cpu_info = CpuInfoSerializer()
	database = DatabaseInfoSerializer()
	cache = CacheInfoSerializer(required=False)
