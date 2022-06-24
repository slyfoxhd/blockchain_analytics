from datetime import datetime
from subgrounds.subgraph import SyntheticField, FieldPath
from subgrounds.subgrounds import Subgrounds
import pandas as pd

sg = Subgrounds()
klima = sg.load_subgraph('https://api.thegraph.com/subgraphs/name/klimadao/klimadao-protocol-metrics')

klima.TreasuryAsset.datetime = SyntheticField(
  lambda timestamp: str(datetime.fromtimestamp(timestamp)),
  SyntheticField.STRING,
  klima.TreasuryAsset.timestamp,
)

klima.ProtocolMetric.datetime = SyntheticField(
  lambda timestamp: str(datetime.fromtimestamp(timestamp)),
  SyntheticField.STRING,
  klima.ProtocolMetric.timestamp,
)

carbon_bct_250d = klima.Query.treasuryAssets(
    where = {'token':'0x2f800db0fdb5223b3c3f354886d907a671414a7f'},
    orderBy = klima.TreasuryAsset.timestamp,
    orderDirection = 'desc',
    first = 250
)

carbon_bct_1d = klima.Query.treasuryAssets(
    where = {'token':'0x2f800db0fdb5223b3c3f354886d907a671414a7f'},
    orderBy = klima.TreasuryAsset.timestamp,
    orderDirection = 'desc',
    first = 1
)


carbon_mco_250d = klima.Query.treasuryAssets(
    where = {'token':'0xaa7dbd1598251f856c12f63557a4c4397c253cea'},
    orderBy = klima.TreasuryAsset.timestamp,
    orderDirection = 'desc',
    first = 250
)

carbon_mco_1d = klima.Query.treasuryAssets(
    where = {'token':'0xaa7dbd1598251f856c12f63557a4c4397c253cea'},
    orderBy = klima.TreasuryAsset.timestamp,
    orderDirection = 'desc',
    first = 1
)

carbon_ubo_250d = klima.Query.treasuryAssets(
    where = {'token':'0x2B3eCb0991AF0498ECE9135bcD04013d7993110c'},
    orderBy = klima.TreasuryAsset.timestamp,
    orderDirection = 'desc',
    first = 250
)

carbon_ubo_1d = klima.Query.treasuryAssets(
    where = {'token':'0x2B3eCb0991AF0498ECE9135bcD04013d7993110c'},
    orderBy = klima.TreasuryAsset.timestamp,
    orderDirection = 'desc',
    first = 1
)

carbon_nbo_250d = klima.Query.treasuryAssets(
    where = {'token':'0x6BCa3B77C1909Ce1a4Ba1A20d1103bDe8d222E48'},
    orderBy = klima.TreasuryAsset.timestamp,
    orderDirection = 'desc',
    first = 250
)

carbon_nbo_1d = klima.Query.treasuryAssets(
    where = {'token':'0x6BCa3B77C1909Ce1a4Ba1A20d1103bDe8d222E48'},
    orderBy = klima.TreasuryAsset.timestamp,
    orderDirection = 'desc',
    first = 1
)

carbon_nct_250d = klima.Query.treasuryAssets(
    where = {'token':'0xD838290e877E0188a4A44700463419ED96c16107'},
    orderBy = klima.TreasuryAsset.timestamp,
    orderDirection = 'desc',
    first = 250
)

carbon_nct_1d = klima.Query.treasuryAssets(
    where = {'token':'0xD838290e877E0188a4A44700463419ED96c16107'},
    orderBy = klima.TreasuryAsset.timestamp,
    orderDirection = 'desc',
    first = 1
)


sum(sg.query_df([
    carbon_bct_1d.carbonBalance,
    carbon_mco_1d.carbonBalance,
    carbon_ubo_1d.carbonBalance,
    carbon_nbo_1d.carbonBalance
]))

klima_supply_1d = klima.Query.protocolMetrics(
    orderBy = klima.ProtocolMetric.timestamp,
    orderDirection = 'desc',
    first = 1
)

klima_supply_250d = klima.Query.protocolMetrics(
    orderBy = klima.ProtocolMetric.timestamp,
    orederDirection = 'desc',
    first = 250
)


carbon_token = sum(sg.query_df([
    carbon_bct_250d.carbonBalance,
    carbon_mco_250d.carbonBalance,
    carbon_ubo_250d.carbonBalance,
    carbon_nbo_250d.carbonBalance
]))

carbon_custodied_250d = klima.Query.protocolMetrics(
    orderby = klima.ProtocolMetric.timestamp,
    orderDirection = 'desc',
    first = 250
)

carbon_custodied_1d = klima.Query.protocolMetrics(
    orderby = klima.ProtocolMetric.timestamp,
    orderDirection = 'desc',
    first = 1
)

carbon_cust = sg.query_df([
    carbon_bct_250d.datetime,
    carbon_custodied_250d.treasuryCarbonCustodied
])

treasury_carbon = pd.concat([carbon_cust[0], carbon_cust[1]], axis=1, ignore_index = True)
treasury_carbon_total = pd.concat([treasury_carbon, carbon_token], axis=1, ignore_index= True)

treasury_carbon_total.rename(columns={0:'timestamp', 1: 'carbon_cust', 2:'carbon_token'}, inplace=True)
treasury_carbon_total['carbon_LPtoken'] = treasury_carbon_total['carbon_cust'] - treasury_carbon_total['carbon_token']
#treasury_carbon_total[treasury_carbon_total['carbon_LPtoken'] < 0] = 0

# A manually crafted dictionary to map asset addresses to their symbol
token_symbol_map = {
    '0x2f800db0fdb5223b3c3f354886d907a671414a7f': 'BCT',
    '0x2B3eCb0991AF0498ECE9135bcD04013d7993110c': 'UBO',
    '0x6BCa3B77C1909Ce1a4Ba1A20d1103bDe8d222E48': 'NBO',
    '0xaa7dbd1598251f856c12f63557a4c4397c253cea': 'MCO',
    '0xD838290e877E0188a4A44700463419ED96c16107': 'NCT',
}


# FieldPath selecting treasury assets from the last day's ProtocolMetric 
# entity. Notice that the assets are filtered so that we only get those in our
# dictionary
treasury_assets = klima.Query.protocolMetrics(
    first=1,
    orderBy=klima.ProtocolMetric.timestamp,
    orderDirection='desc',
).assets(
    where={'token_in': list(token_symbol_map.keys())}
)


# SyntheticField to map the asset address to its symbol. If the token is unknown
# The address is returned
klima.TreasuryAsset.symbol = SyntheticField(
    lambda addr: token_symbol_map[addr] if addr in token_symbol_map else addr,
    SyntheticField.STRING,
    klima.TreasuryAsset.token
)

klima.ProtocolMetric.backing = SyntheticField(
    lambda klima_mcap, carbon_cust: (klima_mcap / carbon_cust),
    SyntheticField.FLOAT,
    [klima.ProtocolMetric.marketCap,
    klima.ProtocolMetric.treasuryCarbonCustodied],
)