import geojson
import folium
from seavoyage.classes.m_network import MNetwork

def map_folium(
        data: dict | geojson.FeatureCollection | MNetwork, 
        center: tuple[float, float] = (36.0, 129.5), 
        zoom: int = 7,
        width: str = '100%',
        height: str = '100%',
    ) -> folium.Map:
    """
    folium 지도 객체 생성
    :param data: geojson 데이터, MNetwork 객체, 또는 geojson dict
    :param center: 지도 중심 좌표
    :param zoom: 지도 초기 확대 정도
    :param width: 지도 너비 (예: '800px' 또는 '100%')
    :param height: 지도 높이 (예: '600px' 또는 '100%')
    :return: folium 지도 객체
    """
    m = folium.Map(
        location=center, 
        zoom_start=zoom,
        width=width,
        height=height
    )
    
    if isinstance(data, MNetwork):
        geojson_data = data.to_geojson()
    else:
        geojson_data = data
        
    folium.GeoJson(geojson_data, name="GeoJSON Layer").add_to(m)
    return m
